import unittest

import torch

from echoflow.core import BatchNorm


class TestBatchNorm(unittest.TestCase):
    def test_basic(self):
        model = BatchNorm(10)

        def test_run(model):
            x = torch.randn((100, 10))

            y, logdet = model(x)
            self.assertTupleEqual(x.size(), y.size())
            self.assertTupleEqual(logdet.size(), (1,))

            x_out, logdet = model(y, inverse=True)
            self.assertTupleEqual(x.size(), x_out.size())
            self.assertTupleEqual(logdet.size(), (1,))

            self.assertTrue((x_out - x).abs().mean() < 1e-6)

        model.train()
        test_run(model)
        model.eval()
        test_run(model)
