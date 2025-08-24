

<!-- Automatically generated, uses README.qmd to modify README.md -->

# `bumplot`: easily create and customize bump charts in Python

<img src="https://github.com/JosephBARBIERDARNAL/static/blob/main/python-libs/bumplot/image.png?raw=true" alt="bumplot logo" align="right" width="180px"/>

`bumplot` is a small Python package made to facilitate the creation of
**bump charts** using matplotlib and Bézier curves. It has high
customization capabilities too!

Bump charts are useful when the focus is on comparing **relative
rankings**—who is ahead of whom—rather than the exact magnitude of the
differences.

Check out the [online
documentation](https://y-sunflower.github.io/bumplot/)

<br> <br>

## Get started

``` python
import matplotlib.pyplot as plt
import pandas as pd

from bumplot import bumplot

data = pd.DataFrame(
    {
        "x": [2020, 2021, 2022, 2023],
        "A": [10, 50, 20, 80],
        "B": [40, 30, 60, 10],
        "C": [90, 20, 70, 40],
    }
)
x = "x"
y_columns = ["A", "B", "C"]

fig, ax = plt.subplots(figsize=(8, 4))
bumplot(
    x=x,
    y_columns=y_columns,
    data=data,
    curve_force=0.5,
    plot_kwargs={"lw": 4},
    scatter_kwargs={"s": 150, "ec": "black", "lw": 2},
    colors=["#ffbe0b", "#ff006e", "#3a86ff"],
)
ax.legend()
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.grid(alpha=0.4)
```

![](README_files/figure-commonmark/cell-2-output-1.png)

[See more examples](https://y-sunflower.github.io/bumplot/examples/)

<br> <br>

## Installation

    pip install bumplot
