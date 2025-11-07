from __future__ import annotations

import numpy as np
import narwhals as nw
from matplotlib.path import Path
from matplotlib.collections import PathCollection
from typing import Any

from .bezier import bezier_curve
from ._utils import _ranked_df

try:
    from plotnine._utils import SIZE_FACTOR, to_rgba
    from plotnine import geom_path
    from plotnine.stats.stat import stat
    from plotnine.doctools import document
except ImportError:
    raise ImportError("plotnine must be installed to use bumplot.geoms")

# TODO:
# curve_force
# ggbump interpolates points for lines on the bezier curve

class stat_rank(stat):
    """Compute the rank of y values within each group.

    This statistic assigns ranks to the y values within each group, which can
    be useful for visualizations that require ranking information.

    Parameters
    ----------
    {common_parameters}

    Examples
    --------


    """

    # TODO: I get an error if I don't set geom here,
    # even though it is not on the base stat class
    DEFAULT_PARAMS = {
        "geom": "TODO",
    }

    def compute_group(self, data, scales):
        return self._calc_rank(data)
    
    @staticmethod
    def _calc_rank(data):
        return (
            nw
            .from_native(data)
            .with_columns(y=nw.col("y").rank(descending=True))
            .to_native()
        )


@document
class geom_bezier(geom_path):
    """Draw a bezier curve between points.

    {usage}

    Parameters
    ----------
    {common_parameters}

    Examples
    --------


    """

    DEFAULT_PARAMS = {
        **geom_path.DEFAULT_PARAMS,
        "curve_force": 0.5,
    }

    @staticmethod
    def draw_group(data, panel_params, coord, ax, params: dict[str, Any]):
        data = coord.transform(data, panel_params, munch=True)
        data["linewidth"] = data["size"] * SIZE_FACTOR

        # fixed parameter curve_force for now
        curve_force = params["curve_force"]

        color = to_rgba(data["color"], data["alpha"])

        indices: list[int] = []
        paths: list[Path] = []

        # Note that this is similar to the Plotnine geom_path non-constant
        # logic, except that it creates a PathCollection, rather than lines.
        for _, df in data.groupby("group"):
            idx = df.index
            indices.extend(idx[:-1].to_list())
            vertices, codes = bezier_curve(data["x"].to_numpy(), df["y"].to_numpy(), curve_force)
            paths.append(Path(vertices, codes))

        d = {
            "edgecolor": color if color is None else [color[i] for i in indices],
            "linewidth": data.loc[indices, "linewidth"],
            "linestyle": data.loc[indices, "linetype"],
            "capstyle": params.get("lineend"),
            "zorder": params["zorder"],
            "rasterized": params["raster"],
            "facecolor": "none",
        }

        coll = PathCollection(paths, **d)
        ax.add_collection(coll)

@document
class geom_bump(geom_bezier):
    """Draw a bump plot using bezier curves between points.

    {usage}

    Parameters
    ----------
    {common_parameters}

    Examples
    --------


    """

    DEFAULT_PARAMS = {
        **geom_bezier.DEFAULT_PARAMS,
        "stat": "rank",
    }