from typing import Optional

import torch
import torch.nn as nn

from .base import BaseFlow


class SequentialFlow(BaseFlow):
    r"""Apply a sequence of flows."""

    def __init__(self, *modules):
        """
        Parameters
        ----------
        *args:
            A list of BaseFlow layers to apply in order.
        """
        super(SequentialFlow, self).__init__()
        self._layers = nn.ModuleList(modules)

    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        self.input_dims = inputs.size(1)
        logdets = torch.zeros(inputs.size(0), 1)

        if not inverse:
            for layer in self._layers:
                inputs, logdet = layer(inputs, contexts, inverse)
                logdets += logdet
        else:
            for layer in reversed(self._layers):
                inputs, logdet = layer(inputs, contexts, inverse)
                logdets += logdet

        return inputs, logdets
