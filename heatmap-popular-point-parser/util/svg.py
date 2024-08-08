import re
import numpy as np
from typing import List

from .cubic_bezier import cubic_bezier


SAMPLING_POINTS = 100


def get_points_from_curve(path_data: str) -> List[tuple[float, float]]:
    # 좌표 추출
    coords = re.findall(r"[-+]?\d*\.\d+|\d+", path_data)
    coords = list(map(float, coords))

    # 시작점 설정
    x0, y0 = coords[0], coords[1]
    points = [(x0, y0)]

    # Cubic Bezier Curve 샘플링
    for i in range(2, len(coords), 6):
        x1, y1 = coords[i], coords[i + 1]
        x2, y2 = coords[i + 2], coords[i + 3]
        x3, y3 = coords[i + 4], coords[i + 5]

        for t in np.linspace(0, 1, SAMPLING_POINTS):
            x = cubic_bezier(t, x0, x1, x2, x3)
            y = cubic_bezier(t, y0, y1, y2, y3)
            points.append((x, y))

        x0, y0 = x3, y3

    return points
