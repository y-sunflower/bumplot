import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.patches import PathPatch

import numpy as np

from narwhals.typing import IntoDataFrame

from bumplot.bezier import bezier_curve
from bumplot._utils import _get_first_n_colors, _ranked_df


def bumplot(
    x: str,
    y_columns: list[str],
    data: IntoDataFrame,
    curve_force: float = 1,
    invert_y_axis: bool = True,
    colors: list | None = None,
    plot_kwargs: dict | None = None,
    scatter_kwargs: dict | None = None,
    ax: Axes | None = None,
) -> Axes:
    """
    Creates bump plot, or bump chart, from multiple numerical
    columns.

    It requires the data to be in wide format (e.g., one column
    per line you want to plot).

    Args:
        x: colname of the x-axis variable
        y_columns: colnames of the y-axis variables
        data: A dataframe
        curve_force: Smoothing factor controlling curve tightness. Higher
            values increase curvature by moving control points further away
            from the anchors.
        invert_y_axis: Whether to invert y axis
        colors: An optional list of colors
        plot_kwargs: Additional arguments passed to `patches.PathPatch()`
        scatter_kwargs: Additional arguments passed to `scatter()`
        ax: The matplotlib Axes used. Default to `plt.gca()`

    Returns:
        The matplotlib Axes with the bump plot
    """
    if ax is None:
        ax: Axes = plt.gca()

    default_plot_kwargs = {"facecolor": "none", "lw": 2}
    if plot_kwargs is None:
        plot_kwargs: dict = {}
    default_plot_kwargs.update(plot_kwargs)

    if scatter_kwargs is None:
        scatter_kwargs: dict = {}

    if colors is None:
        colors: list[str] = _get_first_n_colors(n=len(y_columns))
    else:
        assert len(y_columns) <= len(colors), (
            f"Not enough colors, expected <={len(y_columns)}, found {len(colors)}"
        )

    ranked: IntoDataFrame = _ranked_df(data, x=x, y_columns=y_columns)
    x_values_raw: np.ndarray = np.ravel(ranked.select(x).to_numpy())

    if np.issubdtype(x_values_raw.dtype, np.number):
        x_values = x_values_raw
        x_labels = x_values_raw
    else:
        uniques = list(dict.fromkeys(x_values_raw))  # preserves order
        mapping = {val: i for i, val in enumerate(uniques)}
        x_values = np.array([mapping[val] for val in x_values_raw], dtype=int)
        x_labels = x_values_raw

    for i, col in enumerate(y_columns):
        y_values: np.ndarray = np.ravel(ranked.select(col).to_numpy())
        vertices, codes = bezier_curve(
            x=x_values,
            y=y_values,
            force=curve_force,
        )

        path: Path = Path(vertices=vertices, codes=codes)
        patch: PathPatch = patches.PathPatch(
            path=path,
            edgecolor=colors[i],
            **default_plot_kwargs,
        )
        ax.add_patch(patch)
        ax.scatter(x_values, y_values, color=colors[i], label=col, **scatter_kwargs)

    ticks: list[int] = list(range(1, len(y_columns) + 1))
    if invert_y_axis:
        ax.invert_yaxis()
    else:
        ticks: list[int] = list(reversed(ticks))
    ax.set_yticks(ticks=ticks)
    ax.set_xticks(ticks=np.unique(x_values), labels=np.unique(x_labels))

    return ax
