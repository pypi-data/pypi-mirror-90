# Derived from https://github.com/ikostrikov/pytorch-flows
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from .base import BaseFlow


def get_mask(
    in_features: int, out_features: int, in_flow_features: int, mask_type=None
):
    if mask_type == "input":
        in_degrees = torch.arange(in_features) % in_flow_features
    else:
        in_degrees = torch.arange(in_features) % (in_flow_features - 1)

    if mask_type == "output":
        out_degrees = torch.arange(out_features) % in_flow_features - 1
    else:
        out_degrees = torch.arange(out_features) % (in_flow_features - 1)

    return (out_degrees.unsqueeze(-1) >= in_degrees.unsqueeze(0)).float()


class MaskedLinear(BaseFlow):
    def __init__(
        self,
        input_dims: int,
        out_features: int,
        weight_mask: torch.Tensor,
        context_dims: int = 0,
    ):
        super(MaskedLinear, self).__init__()
        self.weight_mask = weight_mask
        self.linear = nn.Linear(input_dims, out_features)
        if context_dims:
            self.context_linear = nn.Linear(context_dims, out_features)

    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        output = F.linear(
            inputs, self.linear.weight * self.weight_mask, self.linear.bias
        )
        if contexts is not None:
            output += self.context_linear(contexts)
        return output


class MADE(BaseFlow):
    def __init__(self, input_dims, hidden_dims, context_dims=0):
        super(MADE, self).__init__()

        input_mask = get_mask(input_dims, hidden_dims, input_dims, mask_type="input")
        hidden_mask = get_mask(hidden_dims, hidden_dims, input_dims)
        output_mask = get_mask(
            hidden_dims, input_dims * 2, input_dims, mask_type="output"
        )

        self.joiner = MaskedLinear(input_dims, hidden_dims, input_mask, context_dims)

        self.trunk = nn.Sequential(
            nn.LeakyReLU(inplace=True),
            MaskedLinear(hidden_dims, hidden_dims, hidden_mask),
            nn.LeakyReLU(inplace=True),
            MaskedLinear(hidden_dims, input_dims * 2, output_mask),
        )

    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        if not inverse:
            h = self.joiner(inputs, contexts)
            m, a = self.trunk(h).chunk(2, 1)
            u = (inputs - m) * torch.exp(-a)
            return u, -a.sum(-1, keepdim=True)

        else:
            x = torch.zeros_like(inputs)
            for i in range(inputs.shape[1]):
                h = self.joiner(x, contexts)
                m, a = self.trunk(h).chunk(2, 1)
                x[:, i] += inputs[:, i] * torch.exp(a[:, i]) + m[:, i]
            return x, -a.sum(-1, keepdim=True)
