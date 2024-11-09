from typing import List

from subtitle import Subtitle, SubtitleResult


class SubtitleReconstructor:
    MAX_LINE_LENGTH = 20
    DURATION_MIN_THRESHOLD = 0.5
    DURATION_MAX_THRESHOLD = 7

    def reconstruct(self, words: List[Subtitle]) -> SubtitleResult:
        subtitles: List[Subtitle] = []

        current_line: str = ""
        start_time: float = 0
        end_time: float = 0

        for word_data in words:
            current_duration = end_time - start_time

            if self._shouldSplit(current_line, current_duration):
                subtitles.append(Subtitle(subtitle=current_line.strip(), start=start_time, end=end_time))
                current_line = ""
                start_time = word_data.start

            current_line += word_data.subtitle + " "

            if start_time == 0:
                start_time = word_data.start

            end_time = word_data.end

        if current_line:
            subtitles.append(Subtitle(subtitle=current_line.strip(), start=start_time, end=end_time))

        return SubtitleResult(subtitles)

    def _shouldSplit(self, line: str, duration: float):
        if self._isTooShortDuration(duration):
            return False

        return self._isTooLongDuration(duration) \
            or self._isTooLongLine(line)

    def _isTooShortDuration(self, duration: float) -> bool:
        return duration < self.DURATION_MIN_THRESHOLD

    def _isTooLongDuration(self, duration: float) -> bool:
        return duration > self.DURATION_MAX_THRESHOLD

    def _isTooLongLine(self, line: str) -> bool:
        return len(line) > self.MAX_LINE_LENGTH


if __name__ == "__main__":
    reconstructor = SubtitleReconstructor()
    subtitles = reconstructor.reconstruct([
        Subtitle(subtitle="저의", start=3953.985, end=3954.425),
        Subtitle(subtitle="축사는", start=3954.525, end=3954.905),
        Subtitle(subtitle="이만", start=3955.005, end=3955.206),
        Subtitle(subtitle="줄이도록", start=3955.986, end=3956.346),
        Subtitle(subtitle="하겠습니다", start=3956.446, end=3957.587),
        Subtitle(subtitle="그럼", start=3957.707, end=3957.947),
        Subtitle(subtitle="오늘도", start=3958.307, end=3958.987),
        Subtitle(subtitle="좋은", start=3959.188, end=3959.328),
        Subtitle(subtitle="행사", start=3959.368, end=3959.788),
        Subtitle(subtitle="잘", start=3959.928, end=3960.008),
        Subtitle(subtitle="보내시고", start=3960.088, end=3960.508),
        Subtitle(subtitle="행사", start=3961.229, end=3961.449),
        Subtitle(subtitle="준비하시고", start=3961.549, end=3962.109),
        Subtitle(subtitle="또", start=3962.229, end=3962.309),
        Subtitle(subtitle="발표하시는", start=3962.389, end=3963.109),
        Subtitle(subtitle="분들", start=3963.21, end=3963.41),
        Subtitle(subtitle="모두", start=3963.49, end=3963.77),
        Subtitle(subtitle="수고하셨습니다", start=3965.09, end=3965.911),
        Subtitle(subtitle="행사", start=3966.631, end=3966.771),
        Subtitle(subtitle="잘", start=3966.831, end=3966.931),
        Subtitle(subtitle="마무리", start=3966.971, end=3967.131),
        Subtitle(subtitle="하시기", start=3967.211, end=3967.452),
        Subtitle(subtitle="바랍니다", start=3967.512, end=3968.652),
        Subtitle(subtitle="감사합니다", start=3968.672, end=3971.053),
        Subtitle(subtitle="뮤스콘23에", start=3971.273, end=3972.314),
        Subtitle(subtitle="참여하신", start=3972.434, end=3972.934),
        Subtitle(subtitle="개발자분들", start=3973.014, end=3973.595),
        Subtitle(subtitle="반갑습니다", start=3973.675, end=3974.215),
        Subtitle(subtitle="저는", start=3975.255, end=3975.516),
        Subtitle(subtitle="글로벌", start=3975.656, end=3975.916),
    ])

    def to_readable_time(seconds: float) -> str:
        return f"{seconds // 60:02}분 {seconds % 60:06.3f}초"

    for subtitle in subtitles.subtitles:
        print(f"{to_readable_time(subtitle.start)} ~ {to_readable_time(subtitle.end)}: {subtitle.subtitle}")
