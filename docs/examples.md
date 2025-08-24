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

### Heavily styled bump chart

```python
# mkdocs: render
import matplotlib.pyplot as plt
import pandas as pd
from bumplot import bumplot

df = pd.DataFrame(
    {
        "Stage": ["Q1", "Q2", "Q3", "Q4"],
        "Alpha": [4, 3, 2, 1],
        "Beta": [1, 2, 4, 3],
        "Gamma": [2, 1, 3, 4],
    }
)

fig, ax = plt.subplots(figsize=(10, 5))
bumplot(
    x="Stage",
    y_columns=["Alpha", "Beta", "Gamma"],
    data=df,
    curve_force=0.3,
    colors=["#e63946", "#626262ff", "#457b9d"],
    plot_kwargs={"lw": 6, "alpha": 0.7},
    scatter_kwargs={"s": 300, "ec": "black", "lw": 2},
    ax=ax,
)

ax.set_facecolor("#f8f9fa")
ax.legend(frameon=False, ncol=1, bbox_to_anchor=(0, 0.5))
ax.grid(alpha=0.3, ls="--")
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
```
