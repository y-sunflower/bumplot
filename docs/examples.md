### Minimal bump chart with default settings

```python
# mkdocs: render
import matplotlib.pyplot as plt
import pandas as pd
from bumplot import bumplot

df = pd.DataFrame(
    {
        "year": [2019, 2020, 2021, 2022],
        "Team A": [3, 1, 2, 4],
        "Team B": [2, 3, 1, 2],
        "Team C": [1, 2, 3, 1],
    }
)

fig, ax = plt.subplots(figsize=(6, 3))
bumplot(x="year", y_columns=["Team A", "Team B", "Team C"], data=df)
ax.legend()
```

### Stronger curves with custom colors

```python
# mkdocs: render
import matplotlib.pyplot as plt
import pandas as pd
from bumplot import bumplot

df = pd.DataFrame(
    {
        "season": ["S1", "S2", "S3", "S4"],
        "X": [5, 2, 6, 3],
        "Y": [2, 6, 3, 5],
        "Z": [6, 3, 5, 2],
    }
)

fig, ax = plt.subplots(figsize=(7, 4))
bumplot(
    x="season",
    y_columns=["X", "Y", "Z"],
    data=df,
    curve_force=1.5,
    colors=["#d62828", "#f77f00", "#003049"],
    scatter_kwargs={"s": 200, "zorder": 3},
    plot_kwargs={"lw": 3},
)
ax.legend()
```

### Multiple bump plots on subplots

```python
# mkdocs: render
import matplotlib.pyplot as plt
import pandas as pd
from bumplot import bumplot

df = pd.DataFrame(
    {
        "round": [1, 2, 3, 4],
        "P1": [1, 2, 3, 2],
        "P2": [2, 1, 2, 1],
        "P3": [3, 3, 1, 3],
    }
)

fig, axs = plt.subplots(1, 2, figsize=(12, 4))

bumplot(
   x="round",
   y_columns=["P1", "P2"],
   data=df,
   ax=axs[0],
   colors=["#219ebc", "#ffb703"]
)
axs[0].legend()

bumplot(
   x="round",
   y_columns=["P2", "P3"],
   data=df,
   ax=axs[1],
   colors=["#ffb703", "#da5363ff"]
)
axs[1].legend()
```

### Without inverting y-axis

```python
# mkdocs: render
import matplotlib.pyplot as plt
import pandas as pd
from bumplot import bumplot

df = pd.DataFrame(
    {
        "x": [2020, 2021, 2022, 2023],
        "A": [10, 20, 30, 40],
        "B": [40, 30, 20, 10],
    }
)

fig, ax = plt.subplots(figsize=(6, 3))
bumplot(
    x="x",
    y_columns=["A", "B"],
    data=df,
    invert_y_axis=False,
    colors=["#06d6a0", "#118ab2"],
)
ax.legend()
```

### Flexible Styling

```python
# mkdocs: render
import matplotlib.pyplot as plt
import pandas as pd

from bumplot import bumplot, opts, opts_from_color

data = pd.DataFrame(
    {
        "x": [2020, 2021, 2022, 2023],
        "A": [10, 50, 20, 80],
        "B": [40, 30, 60, 10],
        "C": [90, 20, 70, 40],
    }
)

fig, axes = plt.subplots(ncols=2, nrows=2, figsize=(12, 6), layout="constrained")

axes[0, 0].set_title("Basic, no additional options")
bumplot(x="x", y_columns=["A", "B", "C"], data=data, curve_force=0.5, ax=axes[0, 0])

# plot_kwargs & scatter_kwargs to set the default styles for ALL bumps
axes[0, 1].set_title(
    "Plot-wide customizations passed via\ncolors=…, plot_kwargs=…, scatter_kwargs=…"
)
bumplot(
    x="x",
    y_columns=["A", "B", "C"],
    data=data,
    curve_force=0.5,
    ax=axes[0, 1],
    colors=["#ffbe0b", "#ff006e", "#3a86ff"],
    plot_kwargs={"lw": 4},
    scatter_kwargs={"s": 150, "ec": "black", "lw": 2, "marker": "d"},
)

# Customize individual Bumps via the opts(…) helper
# See: `bumplot.opts.BumpOpts` for all keyword arguments one can pass
axes[1, 0].set_title("Color & Style individual lines via opts")
bumplot(
    x="x",
    y_columns=[
        ("A", opts(line_color="#ffbe0b", marker="d", marker_size=140)),
        ("B", opts(line_color="#ff006e", line_style="--")),
        ("C", opts_from_color("#3a86ff", line_width=5, marker_edgecolor="black")),
    ],
    data=data,
    curve_force=0.5,
    ax=axes[1, 0],
)

# Mix individual Bump options with `plot_kwargs` and `scatter_kwargs`
axes[1, 1].set_title("Mix options to create custom charts!")
bumplot(
    x="x",
    y_columns=[
        "A",
        ("B", opts_from_color("#ff006e", zorder=2, line_width=4, marker_size=80)),
        "C",
    ],
    data=data,
    curve_force=0.5,
    ax=axes[1, 1],
    plot_kwargs={"lw": 1, "ec": "gray"},
    scatter_kwargs={"fc": "gray", "ec": "gray", "s": 20},
)

for ax in axes.flat:
    ax.margins(x=0.05)
    ax.spines[["top", "right"]].set_visible(False)

plt.show()
```
