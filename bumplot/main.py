from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection

import numpy as np

from narwhals.typing import IntoDataFrame

from bumplot.bezier import bezier_curve
from bumplot._utils import _ranked_df, _to_ordinal

from typing import Tuple, Union


@dataclass(frozen=True)
class Bump:
    name: str

    line_style: str = "-"
    line_color: str = "lightgrey"
    line_width: float = 2
    line_alpha: float = 1

    marker: str = "o"
    marker_size: float = 40
    marker_alpha: float = 1
    marker_facecolor: str = "black"
    marker_edgecolor: str = "none"
    marker_edgewidth: float = 2

    clip_on: bool = True


def bumplot(
    x: str,
    y_columns: list[Union[Bump, str]],
    data: IntoDataFrame,
    curve_force: float = 1,
    invert_y_axis: bool = True,
    ax: Axes | None = None,
    ordinal_labels: bool = False,
) -> Tuple[Axes, dict[Bump, Tuple[PathPatch, PatchCollection]]]:
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
        ax: The matplotlib Axes used. Default to `plt.gca()`
        ordinal_labels: If True, converts y-axis labels to ordinal numbers (1st, 2nd, 3rd, etc.)
    Returns:
        The matplotlib Axes with the bump plot
    """
    if ax is None:
        ax: Axes = plt.gca()

    y_bumps: list[Bump] = [
        y if isinstance(y, Bump) else Bump(name=y) for y in y_columns
    ]
    ranked: IntoDataFrame = _ranked_df(data, x=x, y_columns=[y.name for y in y_bumps])
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
    for bump in y_bumps:
        y_values: np.ndarray = np.ravel(ranked.select(bump.name).to_numpy())
        vertices, codes = bezier_curve(
            x=x_values,
            y=y_values,
            force=curve_force,
        )

        path: Path = Path(vertices=vertices, codes=codes)
        patch: PathPatch = patches.PathPatch(
            path=path,
            alpha=bump.line_alpha,
            facecolor="none",
            edgecolor=bump.line_color,
            linestyle=bump.line_style,
            linewidth=bump.line_width,
            label=f"_{bump.name}",
            clip_on=bump.clip_on,
        )
        ax.add_patch(patch)

        scatter = ax.scatter(
            x_values,
            y_values,
            label=bump.name,
            marker=bump.marker,
            s=bump.marker_size,
            facecolor=bump.marker_facecolor,
            edgecolor=bump.marker_edgecolor,
            linewidth=bump.marker_edgewidth,
            alpha=bump.marker_alpha,
            clip_on=bump.clip_on,
        )
        artists[bump] = (patch, scatter)

    ticks: list[int] = list(range(1, len(y_bumps) + 1))

    if invert_y_axis:
        ax.invert_yaxis()
    else:
        ticks: list[int] = list(reversed(ticks))

    ax.set_yticks(ticks=ticks)

    labels = (
        [_to_ordinal(tick) for tick in ticks]
        if ordinal_labels
        else [str(tick) for tick in ticks]
    )
    ax.set_yticklabels(labels)

    ax.set_xticks(ticks=np.unique(x_values), labels=np.unique(x_labels))

    return ax, artists
