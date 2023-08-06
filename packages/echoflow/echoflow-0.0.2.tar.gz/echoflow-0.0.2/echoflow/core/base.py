from typing import Optional

import torch
import torch.nn as nn


class BaseFlow(nn.Module):
    def __init__(self):
        r"""Normalizing flow layer."""
        super(BaseFlow, self).__init__()

    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        r"""Transform a batch of data.

        Parameters
        ----------
        inputs:
            The input tensor.
        contexts:
            An optional context tensor (for conditional sampling).
        inverse:
            Whether to apply the direct or inverse transform.

        Returns
        ----------
        outputs: torch.Tensor
            The output tensor.
        logdet: torch.Tensor
            The log-determinant of the Jacobian.
        """
        raise NotImplementedError()
