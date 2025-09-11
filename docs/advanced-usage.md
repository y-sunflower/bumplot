Here you'll find advanced examples of `bumplot`.

- Water source in Africa

```py
# mkdocs: render
import pandas as pd
import matplotlib.pyplot as plt
from pyfonts import set_default_font, load_google_font

from bumplot import bumplot

url = "https://raw.githubusercontent.com/y-sunflower/bumplot/main/docs/data/water-africa.csv"
df = pd.read_csv(url)

def ordinal(n: int) -> str:
    if n == 1:
        return "1st"
    elif n == 2:
        return "2nd"
    elif n == 3:
        return "3rd"
    else:
        return f"{n}th"


highlight_colors = {
    "Zambia": "#2a9d8f",
    "Tanzania": "#bb3e03",
}

last_decade = df.index.max()  # or use 2020
countries = df.loc[last_decade].sort_values(ascending=False).index.to_list()[1:]
colors = [highlight_colors.get(col, "lightgrey") for col in countries]

font = load_google_font("Poppins")
set_default_font(font)


fig, ax = plt.subplots(figsize=(12, 5))
bumplot(
    x="decade",
    y_columns=countries,
    data=df,
    curve_force=0.7,
    colors=colors,
    scatter_kwargs={"s": 150, "clip_on": False},
    plot_kwargs={"lw": 4},
)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.set_xlim(1969, 2020)
ax.tick_params(size=0)
ax.tick_params(axis="x", labelsize=14, pad=10)
ax.set_xticks(ax.get_xticks(), labels=[round(tick) for tick in ax.get_xticks()])
ax.set_yticks(
    [i for i in range(1, len(countries) + 1)],
    [ordinal(i) for i in range(1, len(countries) + 1)],
)

font_bold = load_google_font("Poppins", weight="bold")
for i, country in enumerate(countries):
    ax.text(
        x=2021,
        y=i + 1,
        s=country,
        size=11,
        color=colors[i],
        va="center",
        ha="left",
        font=font_bold,
    )

fig.text(
    x=0.5,
    y=1.02,
    s="# of water sources installations in africa".upper(),
    size=18,
    ha="center",
    va="top",
    font=font_bold,
)
fig.text(
    x=0.5,
    y=0.95,
    s="Ranking of each country based on the total number of water source installations for each decade",
    size=10,
    ha="center",
    va="top",
    color="grey",
    font=load_google_font("Poppins", italic=True),
)
fig.text(
    x=0.12,
    y=0,
    s="Made with bumplot\nGraphic: Joseph Barbier",
    va="top",
    color="grey",
    font=load_google_font("Poppins", italic=True),
    size=10,
)
```
