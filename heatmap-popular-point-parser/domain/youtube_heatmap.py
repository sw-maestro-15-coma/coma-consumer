MAX_SVG_WIDTH = 1000


class YoutubeHeatmap:
    svgs: list[str]
    chapter_widths: list[int]
    total_width: int
    video_length: int

    def __init__(self, svgs: list[str], chapter_widths: list[int], video_length: int):
        self.svgs = svgs
        self.chapter_widths = chapter_widths
        self.total_width = sum(chapter_widths)
        self.video_length = video_length

    def get_time_from_video(self, chapter_idx: int, svg_point: int) -> int:
        prev_video_time = sum(self.get_chapter_time(i) for i in range(chapter_idx))
        video_time = self.get_chapter_time(chapter_idx)
        current_point = svg_point / MAX_SVG_WIDTH * video_time

        return int(prev_video_time + current_point)

    def get_chapter_time(self, index: int) -> float:
        width = self.chapter_widths[index]
        return (width / self.total_width) * self.video_length
