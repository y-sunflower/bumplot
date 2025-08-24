import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.collections import PathCollection

import pandas as pd
import polars as pl

import pytest

import bumplot


def test_version():
    assert bumplot.__version__ == "0.1.0"


@pytest.mark.parametrize("backend", [pd, pl])
@pytest.mark.parametrize("curve_force", [0, 0.5, 1, 5])
@pytest.mark.parametrize("colors", [None, ["#ffbe0b", "#ff006e", "#3a86ff"]])
def test_bumplot(backend, curve_force, colors):
    data = {
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y1": [7, 2, 2, 5, 5, 6, 7, 2, 9, 1],
        "y2": [3, 2, 1, 10, 4, 8, 7, 2, 4, 2],
        "y3": [5, 4, 10, 1, 3, 6, 5, 2, 3, 7],
    }
    df = backend.DataFrame(data)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax2 = bumplot.bumplot(
        x="x",
        y_columns=["y1", "y2", "y3"],
        data=df,
        ax=ax,
        curve_force=curve_force,
        colors=colors,
    )

    assert isinstance(ax2, Axes)
    assert ax == ax2

    artists = ax.get_children()

    pathpatches = [artist for artist in artists if isinstance(artist, PathPatch)]
    assert len(pathpatches) == 3

    pathcollections = [
        artist for artist in artists if isinstance(artist, PathCollection)
    ]
    assert len(pathcollections) == 3


def test_bumplot_error():
    data = {
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y1": [7, 2, 2, 5, 5, 6, 7, 2, 9, 1],
        "y2": [3, 2, 1, 10, 4, 8, 7, 2, 4, 2],
        "y3": [5, 4, 10, 1, 3, 6, 5, 2, 3, 7],
    }
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(6, 4))

    with pytest.raises(
        AssertionError,
        match="Not enough colors, expected <=3, found 2",
    ):
        bumplot.bumplot(
            x="x",
            y_columns=["y1", "y2", "y3"],
            data=df,
            ax=ax,
            colors=["black", "black"],
        )
