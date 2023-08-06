import unittest

import torch

from echoflow.core import Reverse


class TestReverse(unittest.TestCase):
    def test_basic(self):
        model = Reverse(input_dims=4)

        x = torch.FloatTensor(
            [
                [0.0, 0.1, 0.2, 0.4],
                [0.4, 0.1, 0.2, 0.3],
            ]
        )

        y, logdet = model(x)
        self.assertTupleEqual(y.size(), (2, 4))

        x_out, logdet = model(y, inverse=True)
        self.assertTupleEqual(x_out.size(), (2, 4))

        self.assertTrue((x_out - x).abs().mean() < 1e-6)
