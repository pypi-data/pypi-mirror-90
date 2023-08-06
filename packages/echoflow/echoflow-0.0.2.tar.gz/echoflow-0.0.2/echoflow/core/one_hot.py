from typing import List, Optional

import torch

from .base import BaseFlow


class OneHot(BaseFlow):
    def __init__(self, cardinality: List[int]):
        super(OneHot, self).__init__()
        self.cardinality = cardinality
        self.scale = 0.1
        self.input_dims = len(cardinality)
        self.output_dims = sum(cardinality)
        assert all(c > 1 for c in cardinality)

    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        offset = 0
        if not inverse:
            inputs = inputs.type(torch.LongTensor)  # type: ignore
            x = torch.randn(inputs.size(0), self.output_dims) * self.scale
            for i, cardinality in enumerate(self.cardinality):
                x.scatter_(1, (offset + inputs[:, i]).unsqueeze(1), 1)
                offset += cardinality
            return x, 0.0
        else:
            x = torch.LongTensor(inputs.size(0), self.input_dims)
            for i, cardinality in enumerate(self.cardinality):
                x[:, i] = torch.argmax(inputs[:, offset : offset + cardinality], dim=1)
                offset += cardinality
            return x, 0.0
