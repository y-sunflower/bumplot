from typing import Any, TypedDict


class BumpOpts(TypedDict, total=False):
    """
    Typed dictionary describing high-level styling options for a bump plot.

    This type represents a user-facing, backend-agnostic set of visual options
    that can be applied to both line (plot) and marker (scatter) artists.

    All fields are optional. Keys are validated at runtime when constructed via
    `opts()` to ensure only supported options are provided.

    The options are later translated into Matplotlib-specific keyword arguments
    via `get_plot_kwargs()` and `get_scatter_kwargs()`.

    Notes
    -----
    - Keys prefixed with `line_` apply to line artists.
    - Keys prefixed with `marker_` apply to scatter/marker artists.
    - Some options (e.g. `clip_on` and `zorder`) apply to both.
    """

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


# TODO: For >=Python 3.11 (https://docs.python.org/3/library/typing.html#typing.Unpack)
def opts(**kwargs: Any) -> BumpOpts:
    """
    Construct a validated `BumpOpts` mapping from keyword arguments.

    This function enforces that all provided keyword arguments correspond to
    supported `BumpOpts` fields. Any unexpected keys result in a `TypeError`.

    Parameters
    ----------
    **kwargs: Unpack[BumpOpts]
        Keyword arguments corresponding to fields defined on `BumpOpts`.

    Returns
    -------
    BumpOpts
        A typed dictionary containing the validated bump plot options.

    Raises
    ------
    TypeError
        If one or more unsupported keyword arguments are provided.

    Notes
    -----
    This function exists to provide runtime validation for `BumpOpts`,
    which is otherwise only enforced statically by type checkers.
    """
    unsupported_keys = kwargs.keys() - BumpOpts.__annotations__
    if unsupported_keys:
        unsupported_repr = ", ".join(map(repr, sorted(unsupported_keys)))
        msg = f"BumpOpts got unexpected keyword argument(s): {unsupported_repr}"
        raise TypeError(msg)

    return BumpOpts(**kwargs)


def opts_from_color(color, /, **kwargs: Any) -> BumpOpts:
    """
    Construct a `BumpOpts` mapping using a single color applied consistently
    across line and marker components.

    The provided color is applied to:
    - `line_color`
    - `marker_facecolor`
    - `marker_edgecolor`

    Any explicitly provided keyword arguments take precedence over the color-based
    defaults.

    Parameters
    ----------
    color
        The color to apply to line and marker components.
    **kwargs
        Additional or overriding bump plot options (passed to `opts`).

    Returns
    -------
    BumpOpts
        A validated bump plot options mapping.

    See Also
    --------
    opts: Performs keyword validation and construction.
    """
    overrides = ["line_color", "marker_facecolor", "marker_edgecolor"]
    new_kwargs = {k: color for k in overrides} | kwargs
    return opts(**new_kwargs)


def get_plot_kwargs(kwargs: BumpOpts, /) -> dict[str, Any]:
    """
    Extract Matplotlib `plot` keyword arguments from a `BumpOpts` mapping.

    This function translates bump-plot-specific option names into the equivalent
    Matplotlib `Axes.plot` keyword arguments using `bumplot.opts.PLOT_MAPPINGS`.

    Parameters
    ----------
    kwargs: Unpack[BumpOpts]
        A `BumpOpts` mapping containing zero or more plot-related options.

    Returns
    -------
    dict[str, Any]
        A dictionary of Matplotlib-compatible keyword arguments suitable for
        `Axes.patches.PathPatch`.

    Notes
    -----
    - Only keys present in both `kwargs` and `PLOT_MAPPINGS` are included.
    """
    plot_kwargs = {}
    for bump_arg, mpl_arg in PLOT_MAPPINGS.items():
        try:
            plot_kwargs[mpl_arg] = kwargs[bump_arg]  # type: ignore[invalid-key]
        except KeyError:
            pass
    return plot_kwargs


def get_scatter_kwargs(kwargs: BumpOpts, /) -> dict[str, Any]:
    """
    Extract Matplotlib `scatter` keyword arguments from a `BumpOpts` mapping.

    This function translates bump-plot-specific option names into the equivalent
    Matplotlib `Axes.scatter` keyword arguments using `bumplot.opts.SCATTER_MAPPINGS`.

    Parameters
    ----------
    kwargs: Unpack[BumpOpts]
        A `BumpOpts` mapping containing zero or more plot-related options.

    Returns
    -------
    dict[str, Any]
        A dictionary of Matplotlib-compatible keyword arguments suitable for
        `Axes.scatter`.

    Notes
    -----
    - Only keys present in both `kwargs` and `SCATTER_MAPPINGS` are included.
    """
    scatter_kwargs = {}
    for bump_arg, mpl_arg in SCATTER_MAPPINGS.items():
        try:
            scatter_kwargs[mpl_arg] = kwargs[bump_arg]  # type: ignore[invalid-key]
        except KeyError:
            pass
    return scatter_kwargs
