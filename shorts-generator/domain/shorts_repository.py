from abc import ABC, abstractmethod

class ShortsRepository(ABC):
    @abstractmethod
    def post_shorts(self,
                    output_path: str,
                    file_name: str) -> None:
        pass