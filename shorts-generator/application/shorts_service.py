import os

from domain.shorts_processor import ShortsProcessor
from domain.shorts_repository import ShortsRepository
from domain.shorts_thumbnail_maker import ShortsThumbnailMaker
from domain.temp_text_file import TempTextFile
from dto.shorts_request import ShortsRequest
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage


class ShortsService:
    def __init__(self,
                 shorts_processor: ShortsProcessor,
                 shorts_repository: ShortsRepository,
                 shorts_thumbnail_maker: ShortsThumbnailMaker) -> None:
        self.__shorts_processor = shorts_processor
        self.__shorts_repository = shorts_repository
        self.__shorts_thumbnail_maker = shorts_thumbnail_maker

    def make_shorts(self, message: ShortsRequestMessage) -> ShortsResponseMessage:
        temp_text_file = TempTextFile()
        temp_text_file.write_to_file(self.__add_next_line_if_over_10(message.top_title))
        text_path: str = temp_text_file.get_text_path()

        output_path: str = self.__shorts_processor.execute(self.__message_to_request(message, text_path=text_path))
        thumbnail_path: str = self.__shorts_thumbnail_maker.execute(shorts_path=output_path)

        shorts_link: str = self.__shorts_repository.post_shorts(output_path=output_path)
        thumbnail_link: str = self.__shorts_repository.post_thumbnail(thumbnail_path=thumbnail_path)

        self.__remove_all_temp_files([text_path, output_path, thumbnail_path])

        return ShortsResponseMessage(video_id=message.video_id,
                                     shorts_id=message.shorts_id,
                                     shorts_link=shorts_link,
                                     thumbnail_link=thumbnail_link)

    @staticmethod
    def __message_to_request(message: ShortsRequestMessage,
                             text_path: str) -> ShortsRequest:
        return ShortsRequest(s3_url=message.video_s3_url,
                      start=message.start_time,
                      end=message.end_time,
                      text_path=text_path)

    @staticmethod
    def __remove_all_temp_files(path_list: list[str]) -> None:
        try:
            for path in path_list:
                if os.path.isfile(path):
                    os.remove(path)
        except Exception as e:
            raise RuntimeError(e)


    @staticmethod
    def __add_next_line_if_over_10(title: str) -> str:
        if len(title) <= 10:
            return title

        full_length: int = len(title)

        first: str = title[:full_length // 2]
        second: str = title[full_length // 2:]

        return first + '\n' + second
