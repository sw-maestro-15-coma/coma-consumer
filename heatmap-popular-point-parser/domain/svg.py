import re
import numpy as np
from dataclasses import dataclass


SAMPLING_POINTS = 100


@dataclass
class SVGPoint:
    x: float
    y: float


def get_points_from_curve(path_data: str, sampling_points: int = SAMPLING_POINTS) -> list[SVGPoint]:
    # 좌표 추출
    coords = re.findall(r"[-+]?\d*\.\d+|\d+", path_data)
    coords = list(map(float, coords))

    # 시작점 설정
    x0, y0 = coords[0], coords[1]
    points: list[SVGPoint] = [SVGPoint(x0, y0)]

    # Cubic Bezier Curve 샘플링
    for i in range(2, len(coords), 6):
        x1, y1 = coords[i], coords[i + 1]
        x2, y2 = coords[i + 2], coords[i + 3]
        x3, y3 = coords[i + 4], coords[i + 5]

        for t in np.linspace(0, 1, sampling_points):
            x = cubic_bezier(t, x0, x1, x2, x3)
            y = cubic_bezier(t, y0, y1, y2, y3)
            points.append(SVGPoint(x, y))

        x0, y0 = x3, y3

    return points


def cubic_bezier(t: float, p0: float, p1: float, p2: float, p3: float) -> float:
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
