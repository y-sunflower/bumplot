import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import PathPatch
from matplotlib.collections import PathCollection

import pandas as pd
import polars as pl

import pytest
from typing import Any

import bumplot
from bumplot.opts import BumpOpts, _get_plot_kwargs, _get_scatter_kwargs


def verify_plot_kwargs(artist: PathPatch, expected_kwargs: dict[str, Any]):
    for k, v in expected_kwargs.items():
        if k == "edgecolor":
            assert artist.get_edgecolor()[:3] == to_rgb(v)
        else:
            assert getattr(artist, f"get_{k}")() == v


def verify_scatter_kwargs(artist: PathCollection, expected_kwargs: dict[str, Any]):
    assert isinstance(artist, PathCollection)

    for k, v in expected_kwargs.items():
        if k == "marker":
            # Matplotlib ingests the marker identifier and transforms it
            #   we would need to recover/repeat the specific transformations
            #   or normalize back for comparison
            continue
        elif k == "s":
            assert artist.get_sizes()[0] == v
        elif k.endswith("color"):
            assert (getattr(artist, f"get_{k}")()[0, :3] == to_rgb(v)).all()
        else:
            assert getattr(artist, f"get_{k}")() == v


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
def test_bumplot(x, backend, curve_force):
    data = {
        "x": x,
        "y1": [7, 2, 2, 5, 5, 6, 7, 2, 9, 1],
        "y2": [3, 2, 1, 10, 4, 8, 7, 2, 4, 2],
        "y3": [5, 4, 10, 1, 3, 6, 5, 2, 3, 7],
    }
    df = backend.DataFrame(data)

    y_columns = ["y1", "y2", "y3"]
    _, in_ax = plt.subplots(figsize=(6, 4))
    out_ax, bump_artists = bumplot.bumplot(
        x="x",
        y_columns=y_columns,
        data=df,
        ax=in_ax,
        curve_force=curve_force,
    )

    assert in_ax is out_ax
    assert len(bump_artists) == len(y_columns)
    assert bump_artists.keys() == set(y_columns)

    plt.close("all")


@pytest.mark.parametrize(
    "plot_kwargs",
    [
        {},
        {
            "alpha": 0.1,
            "edgecolor": "blue",
            "linestyle": "--",
            "linewidth": 3,
            "clip_on": True,
            "zorder": 2,
        },
    ],
    ids=["no-plot-kwargs", "with-plot-kwargs"],
)
@pytest.mark.parametrize(
    "scatter_kwargs",
    [
        {},
        {
            "marker": "d",
            "alpha": 0.2,
            "edgecolor": "red",
            "facecolor": "orange",
            "linewidth": 0.3,
            "s": 51,
            "clip_on": True,
            "zorder": 3,
        },
    ],
    ids=["no-scatter-kwargs", "with-scatter-kwargs"],
)
@pytest.mark.parametrize(
    "y2_opts",
    [
        bumplot.opts(),
        bumplot.opts(
            marker_facecolor="blue",
            line_width=3,
            line_alpha=0.1,
            marker_alpha=0.6,
        ),
    ],
    ids=["y2-default", "y2-overrides"],
)
def test_bumplot_options(
    plot_kwargs: dict[str, Any], scatter_kwargs: dict[str, Any], y2_opts: BumpOpts
):
    data = {
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y1": [7, 2, 2, 5, 5, 6, 7, 2, 9, 1],
        "y2": [3, 2, 1, 10, 4, 8, 7, 2, 4, 2],
        "y3": [5, 4, 10, 1, 3, 6, 5, 2, 3, 7],
    }
    df = pd.DataFrame(data)

    y_columns = ["y1", ("y2", y2_opts)]
    _, ax = plt.subplots(figsize=(6, 4))
    _, bump_artists = bumplot.bumplot(
        x="x",
        y_columns=y_columns,
        data=df,
        ax=ax,
        scatter_kwargs=scatter_kwargs,
        plot_kwargs=plot_kwargs,
    )
    plt.close("all")

    bump_opts: dict[str, BumpOpts] = dict(
        (y, bumplot.opts()) if isinstance(y, str) else y for y in y_columns
    )
    for name, (path_patch, path_collection) in bump_artists.items():
        local_kwargs = bump_opts[name]
        if name == "y1":
            assert local_kwargs == {}
        verify_plot_kwargs(path_patch, plot_kwargs | _get_plot_kwargs(local_kwargs))
        verify_scatter_kwargs(
            path_collection, scatter_kwargs | _get_scatter_kwargs(local_kwargs)
        )


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
    bumplot.bumplot(
        x="x",
        y_columns=["y1", "y2", "y3", "y4", "y5"],
        data=df,
        ax=ax,
        ordinal_labels=ordinal_labels,
        invert_y_axis=False,
    )

    y_labels = [label.get_text() for label in ax.get_yticklabels()]

    if ordinal_labels:
        assert y_labels == ["5th", "4th", "3rd", "2nd", "1st"], (
            f"Expected ordinal labels, got {y_labels}"
        )
    else:
        assert y_labels == ["5", "4", "3", "2", "1"], (
            f"Expected numeric labels, got {y_labels}"
        )

    plt.close("all")
