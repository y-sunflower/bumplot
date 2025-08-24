import matplotlib.pyplot as plt


def _get_first_n_colors(n=int) -> list[str]:
    colors: list[str] = plt.rcParams["axes.prop_cycle"].by_key()["color"][:n]

    return colors
