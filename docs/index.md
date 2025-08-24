# `bumplot`: easily create and customize bump charts in Python

<br>
<br>

## Quick start

```python
# mkdocs: render
import matplotlib.pyplot as plt
from bumplot import bumplot

import polars as pl

data = pl.DataFrame(
    {
        "x": [2020, 2021, 2022, 2023],
        "A": [10, 50, 20, 80],
        "B": [40, 30, 60, 10],
        "C": [90, 20, 70, 40],
    }
)
x = "x"
y_columns = ["A", "B", "C"]

fig, ax = plt.subplots()
bumplot(
    x=x,
    y_columns=y_columns,
    data=data,
    ax=ax,
    curve_force=0.5,
    plot_kwargs={"lw": 4},
    scatter_kwargs={"s": 150, "ec": "black", "lw": 2},
    colors=["#ffbe0b", "#ff006e", "#3a86ff"],
)
ax.legend()
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.grid(alpha=0.4)
```
