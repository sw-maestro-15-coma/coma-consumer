from abc import ABC, abstractmethod

class ShortsProcessor(ABC):
    @abstractmethod
    def execute(self,
                s3_url: str,
                text_path: str,
                start: str,
                end: str,
                subtitle_path: str) -> str:
        pass