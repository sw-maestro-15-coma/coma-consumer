from abc import ABC, abstractmethod

from dto.shorts_request import ShortsRequest

class ShortsProcessor(ABC):
    @abstractmethod
    def execute(self,
                request: ShortsRequest) -> str:
        pass