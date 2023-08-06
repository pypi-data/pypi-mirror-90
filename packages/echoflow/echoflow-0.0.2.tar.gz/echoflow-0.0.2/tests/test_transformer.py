import unittest

import numpy as np
import pandas as pd

from echoflow.transformer import KDETransformer, SplitTransformer, TableTransformer


class TestKDETransformer(unittest.TestCase):
    def test_kde(self):
        X = np.random.normal(size=100)
        transformer = KDETransformer()
        transformer.fit(X)
        Z = transformer.transform(X)
        X_out = transformer.inverse_transform(Z)
        assert np.abs(X - X_out).max() < 1e-6


class TestTableTransformer(unittest.TestCase):
    def test_transformer(self):
        transformer = TableTransformer(use_kde=False)
        df = pd.DataFrame(
            {
                "x": np.linspace(0.0, 1.0, 100),
                "y": 1.0 - np.linspace(0.0, 1.0, 100),
                "z": ["a", "b", "b", "c"] * 25,
            }
        )
        X = transformer.fit_transform(df)
        df_out = transformer.inverse_transform(X)
        assert np.abs(df_out[["x", "y"]].values - df[["x", "y"]].values).max() < 1e-6
        assert (df_out["z"] == df["z"]).all()


class TestSplitTransformer(unittest.TestCase):
    def test_continuous(self):
        transformer = SplitTransformer(use_kde=True)
        df = pd.DataFrame(
            {
                "x": np.linspace(0.0, 1.0, 100),
                "y": 1.0 - np.linspace(0.0, 1.0, 100),
            }
        )
        continuous, categorical = transformer.fit_transform(df)
        assert tuple(continuous.size()) == (100, 2)
        assert categorical is None

        df_out = transformer.inverse_transform(continuous, categorical)
        assert np.abs(df_out[["x", "y"]].values - df[["x", "y"]].values).max() < 1e-6

    def test_categorical(self):
        transformer = SplitTransformer(use_kde=False)
        df = pd.DataFrame(
            {
                "z": ["a", "b", "b", "c"] * 25,
            }
        )
        continuous, categorical = transformer.fit_transform(df)
        assert continuous is None
        assert tuple(categorical.size()) == (100, 1)

        df_out = transformer.inverse_transform(continuous, categorical)
        assert (df_out["z"] == df["z"]).all()

    def test_both(self):
        transformer = SplitTransformer(use_kde=True)
        df = pd.DataFrame(
            {
                "x": np.linspace(0.0, 1.0, 100),
                "y": 1.0 - np.linspace(0.0, 1.0, 100),
                "z": ["a", "b", "b", "c"] * 25,
            }
        )
        continuous, categorical = transformer.fit_transform(df)
        assert tuple(continuous.size()) == (100, 2)
        assert tuple(categorical.size()) == (100, 1)

        df_out = transformer.inverse_transform(continuous, categorical)
        assert np.abs(df_out[["x", "y"]].values - df[["x", "y"]].values).max() < 1e-6
        assert (df_out["z"] == df["z"]).all()
