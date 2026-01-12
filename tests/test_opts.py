import pytest

from bumplot import opts, opts_from_color
from bumplot.opts import get_plot_kwargs, get_scatter_kwargs


def test_opts_accepts_all_valid_keys():
    kwargs = dict(
        line_alpha=0.5,
        line_color="red",
        line_style="--",
        line_width=2.0,
        marker="o",
        marker_size=10,
        marker_alpha=0.8,
        marker_facecolor="blue",
        marker_edgecolor="black",
        marker_edgewidth=1.5,
        clip_on=True,
        zorder=3,
    )

    assert opts(**kwargs) == kwargs


def test_opts_raise_unknown_key():
    with pytest.raises(TypeError, match="unexpected keyword argument") as exc:
        opts(foo=1)
    msg = str(exc.value)
    assert "'foo'" in msg

    with pytest.raises(TypeError, match="unexpected keyword argument") as exc:
        opts(foo=1, bar=2)

    msg = str(exc.value)
    assert "'bar'" in msg
    assert "'foo'" in msg


def test_opts_accepts_empty():
    assert opts() == {}


def test_opts_from_color_sets_all_color_fields():
    o = opts_from_color("red")

    assert o["line_color"] == "red"
    assert o["marker_facecolor"] == "red"
    assert o["marker_edgecolor"] == "red"


def test_opts_from_color_overriden():
    o = opts_from_color(
        "red",
        marker_facecolor="blue",
    )

    assert o["marker_facecolor"] == "blue"
    assert o["marker_edgecolor"] == "red"
    assert o["line_color"] == "red"


def test_get_scatter_kwargs_basic_mapping():
    bump = opts(
        marker="o",
        marker_size=12,
        marker_alpha=0.6,
        marker_edgewidth=2.0,
        clip_on=False,
    )

    out = get_scatter_kwargs(bump)

    assert out == {
        "marker": "o",
        "s": 12,
        "alpha": 0.6,
        "linewidth": 2.0,
        "clip_on": False,
    }


def test_getters_do_not_mutate_input():
    bump = opts(line_alpha=0.5)
    original = dict(bump)

    get_plot_kwargs(bump)
    get_scatter_kwargs(bump)

    assert bump == original
