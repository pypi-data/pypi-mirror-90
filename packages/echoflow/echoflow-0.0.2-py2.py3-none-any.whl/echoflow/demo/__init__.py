import numpy as np
import pandas as pd


def load_dataset(name="spiral") -> pd.DataFrame:
    """Load the dataset as a dataframe.

    Args:
        name (str): The name of the dataset to load.
    """
    return {
        "spiral": load_spiral,
        "high_low": load_high_low,
    }[name]()


def load_spiral() -> pd.DataFrame:
    """Two-dimensional, continuous."""
    t = np.linspace(0.0, 1.0, num=1000)
    df = pd.DataFrame(
        {
            "x": np.sin(t * 12.0) * t,  # type: ignore
            "y": np.cos(t * 12.0) * t,  # type: ignore
        }
    )
    df["x"] += np.random.normal(loc=0.0, scale=0.1, size=len(df))
    df["y"] += np.random.normal(loc=0.0, scale=0.01, size=len(df))
    return df


def load_high_low() -> pd.DataFrame:
    """Two-dimensional, categorical + continuous.

    The categorical column specifies whether the value is high or low; the
    continuous column contains a high or low value.
    """
    cat = np.random.choice(["low", "high"], size=100)  # type: ignore
    cont = np.random.normal(-0.5, 0.1, size=100) + (cat == "high")
    df = pd.DataFrame(
        {
            "cat": cat,
            "cont": cont,
        }
    )
    return df
