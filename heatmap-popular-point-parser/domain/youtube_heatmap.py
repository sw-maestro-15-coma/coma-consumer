from svg import SVGPoint, get_points_from_curve

MAX_SVG_WIDTH = 1000


class YoutubeHeatmap:
    svgs: list[str]
    __chapter_widths: list[int]
    __total_width: int
    __video_length: int

    def __init__(self, svgs: list[str], chapter_widths: list[int], video_length: int):
        self.svgs = svgs
        self.__chapter_widths = chapter_widths
        self.__total_width = sum(chapter_widths)
        self.__video_length = video_length

    def get_popular_points(self, take: int = 10) -> list[int]:
        svg_points: list[tuple[int, SVGPoint]] = self.__get_points_and_index_from_curve()
        sorted_points = sorted(svg_points, key=lambda p: p[1].y)

        times_of_highest_points: list[int] = [
            self.__get_time_from_video(point[0], point[1])
            for point in sorted_points
        ]

        return self.__get_without_duplicate(times_of_highest_points, take)

    def __get_points_and_index_from_curve(self) -> list[tuple[int, SVGPoint]]:
        points = [(idx, get_points_from_curve(svg)) for idx, svg in enumerate(self.svgs)]
        return [(idx, point) for idx, points in points for point in points]

    def __get_time_from_video(self, chapter_idx: int, svg_point: SVGPoint) -> int:
        prev_video_time = sum(self.__get_chapter_time(i) for i in range(chapter_idx))
        video_time = self.__get_chapter_time(chapter_idx)
        current_point = int(svg_point.x) / MAX_SVG_WIDTH * video_time

        return int(prev_video_time + current_point)

    def __get_chapter_time(self, index: int) -> float:
        width = self.__chapter_widths[index]
        return (width / self.__total_width) * self.__video_length

    def __get_without_duplicate(self, points: list[int], take: int) -> list[int]:
        top_points: list[int] = []

        for point in points:
            if len(top_points) >= take:
                break

            for top_point in top_points:
                if top_point - 60 < point < top_point + 60:
                    break
            else:
                top_points.append(point)

        return top_points
