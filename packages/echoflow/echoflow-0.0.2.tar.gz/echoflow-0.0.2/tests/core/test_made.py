import unittest

import torch

from echoflow.core import MADE


class TestMADE(unittest.TestCase):
    def test_no_context(self):
        model = MADE(input_dims=4, hidden_dims=8)

        x = torch.FloatTensor(
            [
                [0.0, 0.1, 0.2, 0.4],
                [0.4, 0.1, 0.2, 0.3],
            ]
        )

        y, logdet = model(x)
        self.assertTupleEqual(y.size(), (2, 4))
        self.assertTupleEqual(logdet.size(), (2, 1))

        x_out, logdet = model(y, inverse=True)
        self.assertTupleEqual(x_out.size(), (2, 4))
        self.assertTupleEqual(logdet.size(), (2, 1))

        self.assertTrue((x_out - x).abs().mean() < 1e-6)

    def test_with_context(self):
        model = MADE(
            input_dims=4,
            hidden_dims=8,
            context_dims=2,
        )

        x = torch.FloatTensor(
            [
                [0.0, 0.1, 0.2, 0.4],
                [0.4, 0.1, 0.2, 0.3],
            ]
        )
        c = torch.FloatTensor(
            [
                [0.0, 0.1],
                [0.1, 0.1],
            ]
        )

        y, logdet = model(x, c)
        self.assertTupleEqual(y.size(), (2, 4))
        self.assertTupleEqual(logdet.size(), (2, 1))

        x_out, logdet = model(y, c, inverse=True)
        self.assertTupleEqual(x_out.size(), (2, 4))
        self.assertTupleEqual(logdet.size(), (2, 1))

        self.assertTrue((x_out - x).abs().mean() < 1e-6)
