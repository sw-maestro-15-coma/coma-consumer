from abc import ABC, abstractmethod


class ShortsRepository(ABC):
    @abstractmethod
    def post_shorts(self, output_path: str) -> str:
        pass


    @abstractmethod
    def post_thumbnail(self, thumbnail_path: str) -> str:
        pass


    @abstractmethod
    def download_shorts(self, s3_url: str) -> str:
        pass
