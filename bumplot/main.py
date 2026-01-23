from collections import ChainMap
from itertools import cycle

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.cbook import normalize_kwargs
from matplotlib.collections import PathCollection
from matplotlib.patches import PathPatch

import numpy as np

from narwhals.typing import IntoDataFrame

from .bezier import bezier_curve
from ._utils import _ranked_df, _to_ordinal
from .opts import BumpOpts, _get_plot_kwargs, _get_scatter_kwargs

from typing import Any, Iterable, Tuple


def bumplot(
    x: str,
    y_columns: Iterable[str | tuple[str, BumpOpts]],
    data: IntoDataFrame,
    curve_force: float = 1,
    invert_y_axis: bool = True,
    colors: Iterable[str] | None = None,
    plot_kwargs: dict[str, Any] = {},
    scatter_kwargs: dict[str, Any] = {},
    ax: Axes | None = None,
    ordinal_labels: bool = False,
) -> Tuple[Axes, dict[str, Tuple[PathPatch, PathCollection]]]:
    """
    Creates bump plot, or bump chart, from multiple numerical
    columns.

    It requires the data to be in wide format (e.g., one column
    per line you want to plot).

    Args:
        x: colname of the x-axis variable
        y_columns: colnames of the y-axis variables and their plotting options.
        data: A dataframe
        curve_force: Smoothing factor controlling curve tightness. Higher
            values increase curvature by moving control points further away
            from the anchors.
        invert_y_axis: Whether to invert y axis
        colors: An optional list of colors
        plot_kwargs: Additional arguments passed to `patches.PathPatch()`
        scatter_kwargs: Additional arguments passed to `scatter()`
        ax: The matplotlib Axes used. Default to `plt.gca()`
        ordinal_labels: If True, converts y-axis labels to ordinal numbers (1st, 2nd, 3rd, etc.)
    Returns:
        The matplotlib Axes with the bump plot
    """
    _plot_ax: Axes = ax if ax is not None else plt.gca()
    colors_iterable = (
        colors
        if colors is not None
        else plt.rcParams["axes.prop_cycle"].by_key()["color"]
    )

    y_bumps: list[tuple[str, BumpOpts]] = [
        (y, BumpOpts()) if isinstance(y, str) else y for y in y_columns
    ]
    ranked: IntoDataFrame = _ranked_df(data, x=x, y_columns=[y for y, _ in y_bumps])
    x_values_raw: np.ndarray = np.ravel(ranked.select(x).to_numpy())

    if np.issubdtype(x_values_raw.dtype, np.number):
        x_values = x_values_raw
        x_labels = x_values_raw
    else:
        uniques = list(dict.fromkeys(x_values_raw))  # preserves order
        mapping = {val: i for i, val in enumerate(uniques)}
        x_values = np.array([mapping[val] for val in x_values_raw], dtype=int)
        x_labels = x_values_raw

    artists = {}
    for (name, bump_opts), color in zip(y_bumps, cycle(colors_iterable)):
        y_values: np.ndarray = np.ravel(ranked.select(name).to_numpy())
        vertices, codes = bezier_curve(
            x=x_values,
            y=y_values,
            force=curve_force,
        )

        path: Path = Path(vertices=vertices, codes=codes)
        patch: PathPatch = patches.PathPatch(
            path=path,
            facecolor="none",
            **ChainMap(
                _get_plot_kwargs(bump_opts),
                normalize_kwargs(plot_kwargs, PathPatch),
                {"edgecolor": color},
            ),
        )
        _plot_ax.add_patch(patch)

        scatter = _plot_ax.scatter(
            x_values,
            y_values,
            label=name,
            **ChainMap(
                _get_scatter_kwargs(bump_opts),
                normalize_kwargs(scatter_kwargs, PathCollection),
                {"facecolor": color},
            ),
        )
        artists[name] = (patch, scatter)

    ticks: list[int] = list(range(1, len(y_bumps) + 1))

    if invert_y_axis:
        _plot_ax.invert_yaxis()
    else:
        ticks: list[int] = list(reversed(ticks))

    _plot_ax.set_yticks(ticks=ticks)

    labels = (
        [_to_ordinal(tick) for tick in ticks]
        if ordinal_labels
        else [str(tick) for tick in ticks]
    )
    _plot_ax.set_yticklabels(labels)

    _plot_ax.set_xticks(ticks=np.unique(x_values), labels=np.unique(x_labels))

    return _plot_ax, artists
