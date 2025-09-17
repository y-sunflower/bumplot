import matplotlib.pyplot as plt

import narwhals as nw
from narwhals.typing import IntoDataFrame


def _get_first_n_colors(n=int) -> list[str]:
    """
    Get the first n colors from matplotlib rcParams.
    """
    colors: list[str] = plt.rcParams["axes.prop_cycle"].by_key()["color"][:n]
    return colors


def _ranked_df(df: IntoDataFrame, x: str, y_columns: list[str]):
    """
    Convert a dataframe to a ranked version of it.
    """
    df_native = nw.from_native(df).select(nw.col(x), nw.col(y_columns))

    df_native_ranked = (
        df_native.unpivot(on=y_columns, index=x)
        .with_columns(nw.col("value").rank("ordinal", descending=True).over(x))
        .pivot(on="variable", index=x, values="value")
        .select(nw.col(x), nw.col(y_columns))
    )

    return df_native_ranked


def _to_ordinal(n: int) -> str:
    """Convert number to ordinal string (1 -> '1st', 2 -> '2nd', etc.)"""
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"
