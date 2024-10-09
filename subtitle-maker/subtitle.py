from abc import *
from dataclasses import dataclass


@dataclass
class Subtitle:
    start_time: int
    end_time: int
    text: str


@dataclass
class SubtitleResult:
    subtitles: list[Subtitle]


class SubtitleGenerator:
    @abstractmethod
    def generate_subtitle(self, audio_path: str) -> SubtitleResult:
        pass
