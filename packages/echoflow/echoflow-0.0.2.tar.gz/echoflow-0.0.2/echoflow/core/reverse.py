# Derived from https://github.com/ikostrikov/pytorch-flows
from typing import Optional

import numpy as np
import torch

from .base import BaseFlow


class Reverse(BaseFlow):
    """Reversing layer from MADE."""

    def __init__(self, input_dims: int):
        super(Reverse, self).__init__()
        self.idx = np.array(np.arange(input_dims)[::-1])

    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        return inputs[:, self.idx], 0.0
