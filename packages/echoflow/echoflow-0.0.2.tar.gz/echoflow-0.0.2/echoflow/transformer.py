from typing import Optional, Tuple

import numpy as np
import pandas as pd
import torch
from scipy.special import ndtr
from scipy.stats import gaussian_kde


class KDETransformer:
    """Probability integral transform via KDE."""

    def fit(self, X: np.ndarray):
        self.model = gaussian_kde(X)
        self.lower = np.min(X) - 3.0 * np.std(X)
        self.upper = np.max(X) + 3.0 * np.std(X)

    def transform(self, X: np.ndarray) -> np.ndarray:
        stdev = np.sqrt(self.model.covariance[0, 0])
        lower = ndtr((self.lower - self.model.dataset) / stdev)[0]
        uppers = ndtr((X[:, None] - self.model.dataset) / stdev)
        return (uppers - lower).dot(self.model.weights)

    def inverse_transform(self, Z: np.ndarray, maxiter=1000, tol=1e-6) -> np.ndarray:
        low = np.full_like(Z, self.lower)
        high = np.full_like(Z, self.upper)
        for _ in range(maxiter):
            guess = (low + high) / 2.0
            f_guess = self.transform(guess) - Z
            low[f_guess <= 0] = guess[f_guess <= 0]
            high[f_guess >= 0] = guess[f_guess >= 0]
            if (high - low).max() < tol:
                break
        return guess


class TableTransformer:
    """Transform a dataframe into a tensor."""

    dims = 0

    def __init__(self, use_kde):
        self.use_kde = use_kde

    def fit_transform(self, df: pd.DataFrame) -> torch.Tensor:
        """Fit and transform a dataframe into a tensor.

        Continuous values are normalized to the [0.0, 1.0] range and
        categorical values are converted into a one-hot representation.

        Parameters
        ----------
        df:
            The dataframe containing continuous and categorical values.

        Returns
        ----------
        torch.Tensor:
            A tensor representation of the data.
        """
        self.dims = 0
        self.mappings = []
        self.columns = df.columns
        for _, column in enumerate(df.columns):
            if df[column].dtype.kind in "f":
                mapping = {
                    "type": "continuous",
                    "column": column,
                    "dst_idx": self.dims,
                    "min": df[column].min(),
                    "max": df[column].max(),
                }
                if self.use_kde:
                    transformer = KDETransformer()
                    transformer.fit(df[column].values)
                    mapping["transformer"] = transformer
                self.mappings.append(mapping)
                self.dims += 1
            elif df[column].dtype.kind in "O":
                values = set(df[column])
                self.mappings.append(
                    {
                        "type": "categorical",
                        "column": column,
                        "dst_idx": {
                            value: self.dims + i for i, value in enumerate(values)
                        },
                    }
                )
                self.dims += len(values)
            else:
                raise ValueError("Unsupported data type.")
        return self.transform(df)

    def transform(self, df):
        X = torch.zeros(len(df), self.dims)
        for mapping in self.mappings:
            if mapping["type"] == "continuous":
                if "transformer" in mapping:
                    X[:, mapping["dst_idx"]] = torch.FloatTensor(
                        mapping["transformer"].transform(df[mapping["column"]].values)
                    )
                else:
                    X[:, mapping["dst_idx"]] = (
                        torch.FloatTensor(df[mapping["column"]].values) - mapping["min"]
                    ) / (mapping["max"] - mapping["min"])
            elif mapping["type"] == "categorical":
                for value, idx in mapping["dst_idx"].items():
                    X[df[mapping["column"]] == value, idx] = (
                        1.0 + np.random.normal(0.0, 1.0) / 10.0  # type: ignore
                    )
        return X

    def inverse_transform(self, inputs: torch.Tensor) -> pd.DataFrame:
        """Inverse transform a tensor into a dataframe.

        Parameters
        ----------
        inputs:
            The tensor to apply the inverse transform to.
        """
        X = inputs.detach().numpy()
        cols = {}
        for mapping in self.mappings:
            if mapping["type"] == "continuous":
                if "transformer" in mapping:
                    cols[mapping["column"]] = mapping["transformer"].inverse_transform(
                        X[:, mapping["dst_idx"]]
                    )
                else:
                    cols[mapping["column"]] = (
                        X[:, mapping["dst_idx"]] * (mapping["max"] - mapping["min"])
                        + mapping["min"]
                    )
            elif mapping["type"] == "categorical":
                values, indices = zip(*mapping["dst_idx"].items())
                cols[mapping["column"]] = [
                    values[i] for i in np.argmax(X[:, indices], axis=1)
                ]
        return pd.DataFrame(cols, columns=self.columns)


class SplitTransformer:
    def __init__(self, use_kde):
        self.use_kde = use_kde

    def fit_transform(
        self, df: pd.DataFrame
    ) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor]]:
        self.fit(df)
        return self.transform(df)

    def fit(self, df: pd.DataFrame):
        self.meta = {}
        self.cardinality = []
        self.columns = df.columns
        self.continuous_dims = 0
        self.categorical_dims = 0
        for column in df.columns:
            if df[column].dtype.kind in "f":
                self.meta[column] = {
                    "type": "continuous",
                    "idx": self.continuous_dims,
                    "min": df[column].min(),
                    "max": df[column].max(),
                }
                if self.use_kde:
                    transformer = KDETransformer()
                    transformer.fit(df[column].values)
                    self.meta[column]["transformer"] = transformer
                self.continuous_dims += 1
                if self.meta[column]["min"] == self.meta[column]["max"]:
                    raise ValueError(f"The {column} column is constant.")
            elif df[column].dtype.kind in "O":
                v2i = {v: i for i, v in enumerate(set(df[column]))}
                self.meta[column] = {
                    "type": "categorical",
                    "idx": self.categorical_dims,
                    "v2i": v2i,
                    "i2v": {i: v for v, i in v2i.items()},
                }
                self.cardinality.append(len(v2i))
                self.categorical_dims += 1
                if len(v2i) == 1:
                    raise ValueError(f"The {column} column is constant.")
            else:
                raise ValueError("Unsupported data type.")
        if self.continuous_dims == 1:
            self.continuous_dims += 1

    def transform(
        self, df: pd.DataFrame
    ) -> Tuple[Optional[torch.Tensor], Optional[torch.Tensor]]:
        continuous, categorical = None, None
        if self.continuous_dims != 0:
            continuous = torch.zeros(len(df), self.continuous_dims)
        if self.categorical_dims != 0:
            categorical = torch.zeros(len(df), self.categorical_dims)

        for column, meta in self.meta.items():
            if meta["type"] == "continuous":
                assert continuous is not None
                if self.use_kde:
                    continuous[:, meta["idx"]] = torch.FloatTensor(
                        meta["transformer"].transform(df[column].values)
                    )
                else:
                    continuous[:, meta["idx"]] = torch.FloatTensor(
                        (df[column].values - meta["min"]) / (meta["max"] - meta["min"])
                    )
            elif meta["type"] == "categorical":
                assert categorical is not None
                categorical[:, meta["idx"]] = torch.LongTensor(
                    [meta["v2i"][v] for v in df[column].values]
                )
        return continuous, categorical

    def inverse_transform(
        self, continuous: Optional[torch.Tensor], categorical: Optional[torch.Tensor]
    ) -> pd.DataFrame:
        data = {}
        for column, meta in self.meta.items():
            if meta["type"] == "continuous":
                assert continuous is not None
                if self.use_kde:
                    data[column] = meta["transformer"].inverse_transform(
                        continuous[:, meta["idx"]].detach().numpy()
                    )
                else:
                    data[column] = (
                        (
                            continuous[:, meta["idx"]] * (meta["max"] - meta["min"])
                            + meta["min"]
                        )
                        .detach()
                        .numpy()
                    )
                data[column] = np.clip(data[column], meta["min"], meta["max"])
            elif meta["type"] == "categorical":
                assert categorical is not None
                data[column] = [
                    meta["i2v"][i] for i in categorical[:, meta["idx"]].detach().numpy()
                ]
        return pd.DataFrame(data, columns=self.columns)
