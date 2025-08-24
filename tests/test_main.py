import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from bumplot import bumplot


def test_bumplot():
    df = pd.DataFrame(
        data={
            "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "y1": [7, 2, 2, 5, 5, 6, 7, 2, 9, 1],
            "y2": [3, 2, 1, 10, 4, 8, 7, 2, 4, 2],
            "y3": [5, 4, 10, 1, 3, 6, 5, 2, 3, 7],
        }
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax2 = bumplot(
        x="x",
        y_columns=["y1", "y2", "y3"],
        data=df,
        ax=ax,
        curve_force=1,
        colors=["#ffbe0b", "#ff006e", "#3a86ff"],
    )

    assert isinstance(ax2, Axes)
    assert ax == ax2
