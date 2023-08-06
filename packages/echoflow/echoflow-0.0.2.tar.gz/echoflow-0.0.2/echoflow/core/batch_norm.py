# Derived from https://github.com/ikostrikov/pytorch-flows
from typing import Optional, no_type_check

import torch
import torch.nn as nn

from .base import BaseFlow


class BatchNorm(BaseFlow):
    r"""Batch normalization from RealNVP."""

    def __init__(self, input_dims: int, momentum: float = 0.0, eps: float = 1e-5):
        """
        Parameters
        ----------
        input_dims:
            The number of input dimensions.
        momentum:
            The momentum used to compute the running mean/var.
        """
        super(BatchNorm, self).__init__()

        self.log_gamma = nn.Parameter(torch.zeros(input_dims))
        self.beta = nn.Parameter(torch.zeros(input_dims))
        self.momentum = momentum
        self.eps = eps

        self.register_buffer("running_mean", torch.zeros(input_dims))
        self.register_buffer("running_var", torch.ones(input_dims))

    @no_type_check
    def forward(
        self,
        inputs: torch.Tensor,
        contexts: Optional[torch.Tensor] = None,
        inverse: bool = False,
    ):
        if not inverse:
            if self.training:
                self.batch_mean = inputs.mean(0)
                self.batch_var = (inputs - self.batch_mean).pow(2).mean(0) + self.eps

                self.running_mean.mul_(self.momentum)
                self.running_var.mul_(self.momentum)

                self.running_mean.add_(self.batch_mean.data * (1 - self.momentum))
                self.running_var.add_(self.batch_var.data * (1 - self.momentum))

                mean = self.batch_mean
                var = self.batch_var
            else:
                mean = self.running_mean
                var = self.running_var

            x_hat = (inputs - mean) / var.sqrt()
            y = torch.exp(self.log_gamma) * x_hat + self.beta
            return y, (self.log_gamma - 0.5 * torch.log(var)).sum(-1, keepdim=True)

        else:
            if self.training:
                mean = self.batch_mean
                var = self.batch_var
            else:
                mean = self.running_mean
                var = self.running_var

            x_hat = (inputs - self.beta) / torch.exp(self.log_gamma)

            y = x_hat * var.sqrt() + mean

            return y, (-self.log_gamma + 0.5 * torch.log(var)).sum(-1, keepdim=True)
