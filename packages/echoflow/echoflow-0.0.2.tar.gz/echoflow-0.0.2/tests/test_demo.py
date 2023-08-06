import unittest

import numpy as np
import pandas as pd

from echoflow import EchoFlow
from echoflow.demo import load_dataset


class TestDemo(unittest.TestCase):
    def test_spiral(self):
        df = load_dataset("spiral")
        assert len(df.columns) == 2
        model = EchoFlow(nb_epochs=10)
        model.fit(df)
        model.sample(num_samples=10)

    def test_high_low(self):
        df = load_dataset("high_low")
        assert len(df.columns) == 2
        model = EchoFlow(nb_epochs=10)
        model.fit(df)
        model.sample(num_samples=10)
