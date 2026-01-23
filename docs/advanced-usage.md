`bumplot` is designed to integrate seamlessly with matplotlib and allow you to control virtually everything.

Here you will find examples that show how to use `bumplot` in more complex, but also more realistic, cases based on real data.

These examples are also designed to be easy to reproduce: you should be able to simply copy and paste the code onto your computer.

<br>
<br>

- Water sources in Africa

```py
# mkdocs: render
import pandas as pd
import matplotlib.pyplot as plt
from pyfonts import set_default_font, load_google_font

from bumplot import bumplot, opts_from_color

url = "https://raw.githubusercontent.com/y-sunflower/bumplot/main/docs/data/water-africa.csv"
df = pd.read_csv(url)

font = load_google_font("Poppins")
set_default_font(font)

highlight = {
    "Zambia": opts_from_color("#2a9d8f", zorder=2, line_width=3, marker_size=100),
    "Tanzania": opts_from_color("#bb3e03", zorder=2, line_width=3, marker_size=100),
}
countries = [name for name in df.columns if not (name.startswith("decade"))]

fig, ax = plt.subplots(figsize=(12, 5))
_, bump_artists = bumplot(
    x="decade",
    y_columns=[(name, highlight.get(name, {})) for name in countries],
    data=df,
    curve_force=0.7,
    ordinal_labels=True,
    colors=["lightgray"]
)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.margins(x=0.01)
ax.tick_params(size=0)
ax.tick_params(axis="x", labelsize=14, pad=10)
ax.set_xticks(ax.get_xticks(), labels=[round(tick) for tick in ax.get_xticks()])

font_bold = load_google_font("Poppins", weight="bold")
for name, (_, scatter) in bump_artists.items():
    _, last_y = scatter.get_offsets()[-1]
    ax.text(
        x=1,
        y=last_y,
        s=name,
        size=11,
        color=scatter.get_facecolor(),
        va="center",
        ha="left",
        font=font_bold,
        transform=ax.get_yaxis_transform(),
    )

fig.text(
    x=0.5,
    y=0.98,
    s="# of water sources installations in africa".upper(),
    size=18,
    ha="center",
    va="top",
    font=font_bold,
)
fig.text(
    x=0.5,
    y=0.91,
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

plt.show()
```
