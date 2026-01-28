`bumplot` is designed to integrate seamlessly with matplotlib and allow you to control virtually everything.

Here you will find examples that show how to use `bumplot` in more complex, but also more realistic, cases based on real data.

These examples are also designed to be easy to reproduce: you should be able to simply copy and paste the code onto your computer.

<br>
<br>

## Water sources in Africa

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
```

<br>
<br>

## Global CO₂ Emissions Rankings

```py
# mkdocs: render
import pandas as pd
import matplotlib.pyplot as plt
from pyfonts import set_default_font, load_google_font

from bumplot import bumplot, opts_from_color

url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
df_raw = pd.read_csv(url)
countries = [
    "United States",
    "China",
    "India",
    "Russia",
    "Japan",
    "Germany",
    "Iran",
    "South Korea",
    "Saudi Arabia",
    "Indonesia",
]
years = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
df = (
    df_raw[df_raw["country"].isin(countries) & df_raw["year"].isin(years)][
        ["year", "country", "co2"]
    ]
    .dropna()
    .pivot(index="year", columns="country", values="co2")
    .reset_index()
)

font = load_google_font("Inter")
set_default_font(font)

highlight = {
    "China": opts_from_color(
        "#ae2012",
        marker_size=100,
        marker_edgewidth=2,
        zorder=10,
    ),
    "United States": opts_from_color(
        "#005f73",
        marker_size=100,
        marker_edgewidth=2,
        zorder=10,
    ),
}

countries_to_plot = [col for col in df.columns if col != "year"]

fig, ax = plt.subplots(figsize=(10, 7))
_, bump_artists = bumplot(
    x="year",
    y_columns=[(name, highlight.get(name, {})) for name in countries_to_plot],
    data=df,
    curve_force=0.7,
    ordinal_labels=True,
    colors=["#D1D5DB"],
    scatter_kwargs={
        "edgecolor": "#D1D5DB",
        "s": 40,
        "linewidth": 1,
        "facecolor": "#F3F4F6",
    },
    plot_kwargs={"linewidth": 1.5},
)

ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.tick_params(axis="x", labelsize=11, pad=4, colors="#4a4e69")
ax.tick_params(size=0)

font_medium = load_google_font("Inter", weight="medium")
for country in countries:
    if country in bump_artists:
        _, scatter = bump_artists[country]
        _, last_y = scatter.get_offsets()[-1]

        color = "#ae2012" if country == "China" else "#4a4e69"
        weight = "bold" if country == "China" else "regular"
        font_label = load_google_font("Inter", weight=weight)

        ax.text(
            x=1,
            y=last_y,
            s=country,
            size=11,
            color=color,
            va="center",
            ha="left",
            font=font_label,
            transform=ax.get_yaxis_transform(),
        )

font_bold = load_google_font("Inter", weight="bold")
fig.text(
    x=0.5,
    y=0.97,
    s="The Rise of China's CO₂ Emissions",
    size=20,
    ha="center",
    va="top",
    font=font_bold,
    color="#111827",
)
fig.text(
    x=0.5,
    y=0.92,
    s="Ranking of top 10 emitting countries, 1930–2020",
    size=11,
    ha="center",
    va="top",
    color="#4a4e69",
)
fig.text(
    x=0.1,
    y=0.04,
    s="Source: Our World in Data · CO₂ emissions dataset",
    va="bottom",
    ha="left",
    color="#4a4e69",
    size=8,
)
fig.text(
    x=0.9,
    y=0.04,
    s="Made with bumplot",
    va="bottom",
    ha="right",
    color="#4a4e69",
    font=font_bold,
    size=8,
)
```
