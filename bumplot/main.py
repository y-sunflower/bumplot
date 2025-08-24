import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.patches import PathPatch

from narwhals.stable.v2.typing import Frame

from bumplot.bezier import bezier_curve
from bumplot._utils import _get_first_n_colors


def bumplot(
    x: str,
    y_columns: list[str],
    data: Frame,
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

    Args:
        x: colname of the x-axis variable
        y: colnames of the y-axis variables
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

    if plot_kwargs is None:
        plot_kwargs: dict = {}

    if scatter_kwargs is None:
        scatter_kwargs: dict = {}

    if colors is None:
        colors: list[str] = _get_first_n_colors(n=len(y_columns))

    ranked: Frame = data.set_index(x).rank(axis=1, ascending=False, method="first")

    for i, col in enumerate(y_columns):
        vertices, codes = bezier_curve(
            x=ranked.index.values,
            y=ranked[col].values,
            force=curve_force,
        )

        path: Path = Path(vertices=vertices, codes=codes)
        patch: PathPatch = patches.PathPatch(
            path=path,
            facecolor="none",
            lw=2,
            edgecolor=colors[i],
            **plot_kwargs,
        )
        ax.add_patch(patch)
        ax.scatter(ranked.index, ranked[col], color=colors[i], **scatter_kwargs)

    ticks: list[int] = list(range(1, len(y_columns) + 1))
    if invert_y_axis:
        ax.invert_yaxis()
    else:
        ticks: list[int] = list(reversed(ticks))
    ax.set_yticks(ticks=ticks)

    return ax
