from abc import *
from dataclasses import dataclass


@dataclass
class Subtitle:
    start: int
    end: int
    subtitle: str


@dataclass
class SubtitleResult:
    subtitles: list[Subtitle]


class SubtitleGenerator:
    @abstractmethod
    def generate_subtitle(self, audio_path: str) -> SubtitleResult:
        pass
