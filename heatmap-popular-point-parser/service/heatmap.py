from typing import List
from ..util.svg import get_points_from_curve
from ..domain.youtube_heatmap import YoutubeHeatmap


def get_popular_point_by_heatmap(heatmap: YoutubeHeatmap, take: int = 10):
    points = [(idx, get_points_from_curve(svg)) for idx, svg in enumerate(heatmap.svgs)]
    flattened_points = [(idx, point) for idx, points in points for point in points]

    highest_points = sorted(flattened_points, key=lambda p: p[1][1])

    times_of_highest_points = [
        heatmap.get_time_from_video(point[0], int(point[1][0]))
        for point in highest_points
    ]

    return get_without_duplicate(times_of_highest_points, take)


def get_without_duplicate(points: List[int], take: int) -> List[int]:
    top_points = []

    for point in points:
        if len(top_points) >= take:
            break

        for top_point in top_points:
            if top_point - 60 < point < top_point + 60:
                break
        else:
            top_points.append(point)

    return top_points
