from __future__ import annotations

import numpy as np
import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.collections import PathCollection
from matplotlib.patches import PathPatch
from typing import Any

from .main import bumplot
from .bezier import bezier_curve

try:
    from plotnine._utils import SIZE_FACTOR, to_rgba
    from plotnine import geom_path
    from plotnine.doctools import document
except ImportError:
    raise ImportError("plotnine must be installed to use bumplot.geoms")


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

        # TODO: constant currently unused, but copied from plotnine
        if "constant" in params:
            constant: bool = params.pop("constant")
        else:
            constant = len(np.unique(data["group"].to_numpy())) == 1
        
        color = to_rgba(data["color"], data["alpha"])

        indices: list[int] = []
        paths: list[Path] = []

        # TODO: this assumes not constant
        # but plotnine has handling for constant....
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

