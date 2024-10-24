from abc import ABC, abstractmethod


class ShortsThumbnailMaker(ABC):
    @abstractmethod
    def execute(self, shorts_path: str) -> str:
        pass