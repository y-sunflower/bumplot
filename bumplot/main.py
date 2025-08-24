import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.axes import Axes

from narwhals.stable.v2.typing import Frame

from bumplot._utils import _get_first_n_colors


def bezier_curve(ax, x, y, color, force, plot_kwargs):
    vertices: list = []
    codes: list = []

    vertices.append((x[0], y[0]))
    codes.append(Path.MOVETO)

    for i in range(1, len(x)):
        x0, y0 = x[i - 1], y[i - 1]
        x1, y1 = x[i], y[i]
        dx = (x1 - x0) * force

        vertices.extend([(x0 + dx, y0), (x1 - dx, y1), (x1, y1)])
        codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])

    path: Path = Path(vertices=vertices, codes=codes)
    patch: PathPatch = patches.PathPatch(
        path=path,
        facecolor="none",
        lw=2,
        edgecolor=color,
    )
    ax.add_patch(patch)


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
        bezier_curve(
            ax=ax,
            x=ranked.index.values,
            y=ranked[col].values,
            color=colors[i],
            force=curve_force,
            plot_kwargs=plot_kwargs,
        )
        ax.scatter(ranked.index, ranked[col], color=colors[i], **scatter_kwargs)

    ax.invert_yaxis()
    ax.set_yticks(list(range(1, len(y_columns) + 1)))

    return ax
