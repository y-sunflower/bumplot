import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.collections import PathCollection

import pandas as pd
import polars as pl

import pytest

import bumplot


def test_version():
    assert bumplot.__version__ == "0.1.1"


@pytest.mark.parametrize(
    "x",
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    ],
)
@pytest.mark.parametrize("backend", [pd, pl])
@pytest.mark.parametrize("curve_force", [0, 0.5, 1, 5])
@pytest.mark.parametrize("colors", [None, ["#ffbe0b", "#ff006e", "#3a86ff"]])
def test_bumplot(x, backend, curve_force, colors):
    data = {
        "x": x,
        "y1": [7, 2, 2, 5, 5, 6, 7, 2, 9, 1],
        "y2": [3, 2, 1, 10, 4, 8, 7, 2, 4, 2],
        "y3": [5, 4, 10, 1, 3, 6, 5, 2, 3, 7],
    }
    df = backend.DataFrame(data)

    _, ax = plt.subplots(figsize=(6, 4))
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

    plt.close("all")


def test_bumplot_error():
    data = {
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y1": [7, 2, 2, 5, 5, 6, 7, 2, 9, 1],
        "y2": [3, 2, 1, 10, 4, 8, 7, 2, 4, 2],
        "y3": [5, 4, 10, 1, 3, 6, 5, 2, 3, 7],
    }
    df = pd.DataFrame(data)
    _, ax = plt.subplots(figsize=(6, 4))

    with pytest.raises(
        ValueError,
        match="Not enough colors: expected at least 3, but got 2",
    ):
        bumplot.bumplot(
            x="x",
            y_columns=["y1", "y2", "y3"],
            data=df,
            ax=ax,
            colors=["black", "black"],
        )

    plt.close("all")


@pytest.mark.parametrize("ordinal_labels", [True, False])
def test_bumplot_ordinal_labels(ordinal_labels):
    """Test that ordinal labels work correctly"""
    data = {
        "x": [1, 2, 3, 4, 5],
        "y1": [1, 2, 3, 4, 5],
        "y2": [5, 4, 3, 2, 1],
        "y3": [2, 3, 4, 5, 1],
        "y4": [3, 4, 5, 1, 2],
        "y5": [4, 5, 1, 2, 3],
    }
    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots()
    ax = bumplot.bumplot(
        x="x",
        y_columns=["y1", "y2", "y3", "y4", "y5"],
        data=df,
        ax=ax,
        ordinal_labels=ordinal_labels,
        invert_y_axis=False,
    )
    
    y_labels = [label.get_text() for label in ax.get_yticklabels()]
    
    if ordinal_labels:
        assert "1st" in y_labels
        assert "2nd" in y_labels
        assert "3rd" in y_labels
        assert "4th" in y_labels
        assert "5th" in y_labels
    else:
        assert all(label.isdigit() for label in y_labels)
    
    plt.close("all")