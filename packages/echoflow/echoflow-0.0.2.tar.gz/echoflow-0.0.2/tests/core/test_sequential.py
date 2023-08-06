import unittest

import torch

from echoflow.core import MADE, BatchNorm, Coupling, Reverse, SequentialFlow


class TestSequentialFlow(unittest.TestCase):
    def test_rnvp_flow(self):
        model = SequentialFlow(
            Coupling(4, 16, input_mask=torch.LongTensor([0, 1, 0, 1])),
            BatchNorm(4),
            Coupling(4, 16, input_mask=torch.LongTensor([1, 0, 1, 0])),
        )

        x = torch.randn((100, 4))

        y, logdet = model(x)
        self.assertTupleEqual(x.size(), y.size())
        self.assertTupleEqual(logdet.size(), (x.size(0), 1))

        x_out, logdet = model(y, inverse=True)
        self.assertTupleEqual(x.size(), x_out.size())
        self.assertTupleEqual(logdet.size(), (x.size(0), 1))

        self.assertTrue((x_out - x).abs().mean() < 1e-6)

    def test_made_flow(self):
        model = SequentialFlow(
            MADE(4, 16),
            BatchNorm(4),
            Reverse(4),
            MADE(4, 16),
            BatchNorm(4),
        )

        x = torch.randn((100, 4))

        y, logdet = model(x)
        self.assertTupleEqual(x.size(), y.size())
        self.assertTupleEqual(logdet.size(), (x.size(0), 1))

        x_out, logdet = model(y, inverse=True)
        self.assertTupleEqual(x.size(), x_out.size())
        self.assertTupleEqual(logdet.size(), (x.size(0), 1))

        self.assertTrue((x_out - x).abs().mean() < 1e-6)
