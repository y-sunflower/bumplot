from typing import Any, TypedDict


class BumpOpts(TypedDict, total=False):
    line_alpha: float
    line_color: str
    line_style: str
    line_width: float

    marker: str
    marker_size: float
    marker_alpha: float
    marker_facecolor: str
    marker_edgecolor: str
    marker_edgewidth: float

    clip_on: bool
    zorder: int


PLOT_MAPPINGS: dict[str, str] = {
    "line_alpha": "alpha",
    "line_color": "edgecolor",
    "line_style": "linestyle",
    "line_width": "linewidth",
    "clip_on": "clip_on",
    "zorder": "zorder",
}

SCATTER_MAPPINGS: dict[str, str] = {
    "marker": "marker",
    "marker_alpha": "alpha",
    "marker_edgecolor": "edgecolor",
    "marker_edgewidth": "linewidth",
    "marker_facecolor": "facecolor",
    "marker_size": "s",
    "clip_on": "clip_on",
    "zorder": "zorder",
}


def opts(**kwargs: Any) -> BumpOpts:
    unsupported_keys = kwargs.keys() - BumpOpts.__annotations__
    if unsupported_keys:
        msg = f"BumpOpts got unexpected keyword argument(s) {unsupported_keys}"
        raise TypeError(msg)

    return BumpOpts(**kwargs)


def opts_from_color(color, **kwargs: Any) -> BumpOpts:
    overrides = ["line_color", "marker_facecolor", "marker_edgecolor"]
    new_kwargs = {**{k: color for k in overrides}, **kwargs}
    return opts(**new_kwargs)


def get_plot_kwargs(kwargs: BumpOpts, /) -> dict[str, Any]:
    plot_kwargs = {}
    for bump_arg, mpl_arg in PLOT_MAPPINGS.items():
        try:
            plot_kwargs[mpl_arg] = kwargs[bump_arg]  # type: ignore[invalid-key]
        except KeyError:
            pass
    return plot_kwargs


def get_scatter_kwargs(kwargs: BumpOpts, /) -> dict[str, Any]:
    scatter_kwargs = {}
    for bump_arg, mpl_arg in SCATTER_MAPPINGS.items():
        try:
            scatter_kwargs[mpl_arg] = kwargs[bump_arg]  # type: ignore[invalid-key]
        except KeyError:
            pass
    return scatter_kwargs
