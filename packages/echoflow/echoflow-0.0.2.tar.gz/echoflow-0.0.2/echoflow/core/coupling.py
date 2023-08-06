# Derived from https://github.com/ikostrikov/pytorch-flows
from typing import Optional

import torch
import torch.nn as nn

from .base import BaseFlow


class Coupling(BaseFlow):
    r"""Coupling layer from RealNVP.

    The coupling layer partitions the input `x` into two parts, x1 and x2, 
    and applies an invertible transform:

    .. math::

        y1 &= x1 \\
        y2 &= x2 * exp(s(x1)) + t(x1)

    which modifies only one of the partitions.
    """

    def __init__(
        self,
        input_dims: int,
        hidden_dims: int,
        input_mask: torch.Tensor,
        context_dims: int = 0,
    ):
        """
        Parameters
        ----------
        input_dims:
            The number of input dimensions.
        hidden_dims:
            The hidden size to use for the scale/translate nets.
        input_mask:
            A binary mask for the input.
        context_dims:
            The number of context dimensions. If specified, then the output
            is conditioned on context.
        """
        super(Coupling, self).__init__()

        self.input_dims = input_dims
        self.input_mask = input_mask
        assert (
            input_mask.size(0) == input_dims
        ), "Expected input_mask to have size input_dims."

        self.scale_net = nn.Sequential(
            nn.Linear(input_dims + context_dims, hidden_dims),
            nn.Tanh(),
            nn.Linear(hidden_dims, hidden_dims),
            nn.Tanh(),
            nn.Linear(hidden_dims, input_dims),
        )
        self.translate_net = nn.Sequential(
            nn.Linear(input_dims + context_dims, hidden_dims),
            nn.LeakyReLU(inplace=True),
            nn.Linear(hidden_dims, hidden_dims),
            nn.LeakyReLU(inplace=True),
            nn.Linear(hidden_dims, input_dims),
        )

    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        assert inputs.dim() == 2, "Expected tensor of shape (batch_size, input_dims)."
        if contexts is not None:
            assert (
                contexts.dim() == 2
            ), "Expected tensor of shape (batch_size, context_dims)."

        masked_inputs = inputs * self.input_mask
        if contexts is not None:
            masked_inputs = torch.cat([masked_inputs, contexts], -1)

        if not inverse:
            log_s = self.scale_net(masked_inputs) * (1 - self.input_mask)
            t = self.translate_net(masked_inputs) * (1 - self.input_mask)
            s = torch.exp(log_s)
            return inputs * s + t, log_s.sum(-1, keepdim=True)

        else:
            log_s = self.scale_net(masked_inputs) * (1 - self.input_mask)
            t = self.translate_net(masked_inputs) * (1 - self.input_mask)
            s = torch.exp(-log_s)
            return (inputs - t) * s, -log_s.sum(-1, keepdim=True)
