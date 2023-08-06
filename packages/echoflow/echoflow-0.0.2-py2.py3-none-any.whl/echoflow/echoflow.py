import math
from typing import Optional

import pandas as pd
import torch
import torch.optim as optim
from torch.utils.data import Dataset

from echoflow.core import MADE, BatchNorm, Coupling, OneHot, Reverse, SequentialFlow
from echoflow.transformer import SplitTransformer, TableTransformer


class FlowDataset(Dataset):
    def __init__(self, continuous, categorical, contexts):
        self.continuous = continuous
        self.categorical = categorical
        self.contexts = contexts

    def __len__(self):
        if self.continuous is not None:
            return len(self.continuous)
        if self.categorical is not None:
            return len(self.categorical)

    def __getitem__(self, idx):
        continuous = None if self.continuous is None else self.continuous[idx]
        categorical = None if self.categorical is None else self.categorical[idx]
        contexts = None if self.contexts is None else self.contexts[idx]
        return continuous, categorical, contexts


class EchoFlow:
    """Wrapper for training normalizing flow models."""

    def __init__(
        self,
        lr: float = 0.0001,
        nb_epochs: int = 1000,
        batch_size: int = 100,
        nb_blocks: int = 3,
        block_type: str = "RNVP",
        use_kde: bool = False,
    ):
        self.lr = lr
        self.nb_blocks = nb_blocks
        self.nb_epochs = nb_epochs
        self.batch_size = batch_size
        self.block_type = block_type
        self.use_kde = use_kde

    def fit(self, df: pd.DataFrame, context: Optional[pd.DataFrame] = None):
        """Fit the flow model.

        Parameters
        ----------
        df:
            The dataframe containing the samples to model.
        contexts:
            The (optional) context dataframe for conditional sampling.
        """
        self.has_context = context is not None

        self.df_transformer = SplitTransformer(self.use_kde)
        continuous, categorical = self.df_transformer.fit_transform(df)
        self.input_dims = self.df_transformer.continuous_dims + sum(
            self.df_transformer.cardinality
        )

        self.context_transformer = TableTransformer(self.use_kde)
        contexts = (
            self.context_transformer.fit_transform(context)
            if context is not None
            else None
        )

        layers = []
        for _ in range(self.nb_blocks):
            if self.block_type == "RNVP":
                input_mask = torch.arange(0, self.input_dims) % 2
                layers.extend(
                    [
                        Coupling(
                            self.input_dims,
                            100,
                            input_mask,
                            self.context_transformer.dims,
                        ),
                        BatchNorm(self.input_dims),
                        Coupling(
                            self.input_dims,
                            100,
                            1.0 - input_mask,
                            self.context_transformer.dims,
                        ),
                        BatchNorm(self.input_dims),
                    ]
                )
            else:
                layers.extend(
                    [
                        MADE(
                            self.input_dims,
                            100,
                            self.context_transformer.dims,
                        ),
                        BatchNorm(self.input_dims),
                        Reverse(self.input_dims),
                    ]
                )
        self.flow = SequentialFlow(*layers)
        self.flow.train()

        dataset = FlowDataset(continuous, categorical, contexts)
        if categorical is not None:
            self.categorical_encoder = OneHot(self.df_transformer.cardinality)

        def collate_fn(data):
            continuous, categorical, contexts = zip(*data)
            continuous = (
                None if continuous[0] is None else torch.stack(continuous, dim=0)
            )
            categorical = (
                None if categorical[0] is None else torch.stack(categorical, dim=0)
            )
            contexts = None if contexts[0] is None else torch.stack(contexts, dim=0)
            return continuous, categorical, contexts

        dataloader = torch.utils.data.DataLoader(
            dataset, batch_size=self.batch_size, shuffle=True, collate_fn=collate_fn
        )

        optimizer = optim.Adam(self.flow.parameters(), lr=self.lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, "min")
        for epoch in range(1, self.nb_epochs + 1):
            train_loss = []
            for _, (continuous, categorical, contexts) in enumerate(dataloader):
                optimizer.zero_grad()
                loss = torch.zeros(1)

                inputs = []
                if continuous is not None:
                    inputs.append(continuous)
                if categorical is not None:
                    categorical, _loss = self.categorical_encoder(categorical)
                    inputs.append(categorical)  # type: ignore
                    loss += _loss
                inputs = torch.cat(inputs, dim=1)

                loss -= self._log_likelihood(inputs, contexts).mean()

                loss.backward()
                train_loss.append(loss.item())
                optimizer.step()
            train_loss = sum(train_loss) / len(train_loss)
            scheduler.step(train_loss)
            if epoch % 10 == 0:
                print(f"Epoch {epoch} | Train Loss {train_loss:.3f}")

    def sample(
        self, num_samples: Optional[int] = None, context: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """Generate samples via the inverse transform.

        Either `num_samples` or `contexts` must be provided. If both are provided, then
        they must be consistent (i.e. there are `num_samples` rows in `contexts`).

        Parameters
        ----------
        num_samples:
            The number of samples.
        contexts:
            The (optional) context dataframe for conditional sampling.
        """
        if self.has_context:
            assert context is not None
        contexts = (
            self.context_transformer.transform(context) if context is not None else None
        )

        if num_samples is None:
            assert contexts is not None
            num_samples = contexts.size(0)
        elif contexts is not None:
            assert num_samples == contexts.size(0)

        self.flow.eval()
        noise = torch.randn(num_samples, self.input_dims)
        samples, _ = self.flow(noise, contexts, inverse=True)

        continuous, categorical = None, None
        if self.df_transformer.continuous_dims:
            continuous = samples[:, : self.df_transformer.continuous_dims]
        if self.df_transformer.categorical_dims:
            categorical, _ = self.categorical_encoder(
                samples[:, self.df_transformer.continuous_dims :], inverse=True
            )

        return self.df_transformer.inverse_transform(continuous, categorical)

    def log_likelihood(self, df: pd.DataFrame, context: Optional[pd.DataFrame] = None):
        """Compute the log-likelihood of the data.

        Parameters
        ----------
        df:
            The dataframe containing the samples to model.
        contexts:
            The (optional) context dataframe. If it was provided in the fit method, it
            must be provided here as well.
        """
        if self.has_context:
            assert context is not None

        continuous, categorical = self.df_transformer.fit_transform(df)
        contexts = (
            self.context_transformer.transform(context) if context is not None else None
        )

        inputs = []
        if continuous is not None:
            inputs.append(continuous)
        if categorical is not None:
            categorical, _ = self.categorical_encoder(categorical)
            inputs.append(categorical)  # type: ignore
        inputs = torch.cat(inputs, dim=1)

        return self._log_likelihood(inputs, contexts)

    def _log_likelihood(
        self, inputs: torch.Tensor, contexts: Optional[torch.Tensor] = None
    ):
        """Compute the log-likelihood to be maximized.

        Parameters
        ----------
        inputs:
            The input tensor.
        contexts:
            An optional context tensor (for conditional sampling). If it was
            provided in the fit method, it must be provided here as well.
        """
        u, log_jacob = self.flow(inputs, contexts)
        log_probs = (-0.5 * u.pow(2) - 0.5 * math.log(2 * math.pi)).sum(
            -1, keepdim=True
        )
        return (log_probs + log_jacob).sum(-1, keepdim=True)
