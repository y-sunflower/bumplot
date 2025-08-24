from matplotlib.path import Path
import numpy as np


def bezier_curve(
    x: np.ndarray,
    y: np.ndarray,
    force: float,
) -> tuple[list[tuple[float, float]], list[int]]:
    """
    Generate vertices and path codes for a smooth cubic Bézier curve
    passing through a sequence of points.

    This function is used under the hood by [`bumplot()`](./bumplot.md),
    but you can use it too.

    Args:
        x: X-coordinates of the points.
        y: Y-coordinates of the points.
        force: Smoothing factor controlling curve tightness. Higher values
            increase curvature by moving control points further away
            from the anchors.

    Returns:
        vertices: List of (x, y) vertices including control points for the Bézier segments.
        codes: Corresponding matplotlib Path codes for constructing the curve.
    """
    vertices: list = []
    codes: list = []

    vertices.append((x[0], y[0]))
    codes.append(Path.MOVETO)

    for i in range(1, len(x)):
        x0, y0 = x[i - 1], y[i - 1]
        x1, y1 = x[i], y[i]
        dx = (x1 - x0) * force

        vertices.extend([(x0 + dx, y0), (x1 - dx, y1), (x1, y1)])
        codes.extend([Path.CURVE4, Path.CURVE4, Path.CURVE4])

    return vertices, codes
