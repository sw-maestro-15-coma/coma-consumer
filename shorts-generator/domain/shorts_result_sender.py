from abc import ABC, abstractmethod

from dto.shorts_response_message import ShortsResponseMessage

class ShortsResultSender(ABC):
    @abstractmethod
    def send_success(self,
                     shorts_response_message: ShortsResponseMessage) -> None:
        pass

    @abstractmethod
    def send_fail(self,
                  message: str,
                  shorts_id: int) -> None:
        pass