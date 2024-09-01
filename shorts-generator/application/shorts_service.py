import os
from typing import AnyStr

from config import Config
from domain.id_generator import IdGenerator
from domain.shorts_processor import ShortsProcessor
from domain.shorts_repository import ShortsRepository
from dto.shorts_request import ShortsRequest
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage

class ShortsService:
    __S3_URL = Config.s3_url()

    def __init__(self,
                 shorts_processor: ShortsProcessor,
                 id_generator: IdGenerator,
                 shorts_repository: ShortsRepository) -> None:
        self.shorts_processor = shorts_processor
        self.id_generator = id_generator
        self.shorts_repository = shorts_repository

    def make_shorts(self, message: ShortsRequestMessage) -> ShortsResponseMessage:
        uuid: int = self.id_generator.make_id()

        text_path: str = self.__make_temp_text_path(uuid=uuid,
                                               top_title=message.top_title)
        output_path: str = self.__make_temp_output_path(uuid=uuid)

        self.shorts_processor.execute(self.__message_to_request(message,
                                                                text_path=text_path,
                                                                output_path=output_path))
        self.shorts_repository.post_shorts(output_path=output_path, file_name=f"{uuid}.mp4")


        self.__remove_temp_files(text_path=text_path,
                                 output_path=output_path)

        return ShortsResponseMessage(video_id=message.video_id,
                                     shorts_id=message.shorts_id,
                                     link=self.__S3_URL + f"process/{uuid}.mp4")

    @staticmethod
    def __message_to_request(message: ShortsRequestMessage,
                             text_path: str,
                             output_path: str) -> ShortsRequest:
        return ShortsRequest(s3_url=message.video_s3_url,
                      start=message.start_time,
                      end=message.end_time,
                      text_path=text_path,
                      output_path=output_path)

    @staticmethod
    def __remove_temp_files(text_path: str, output_path: str) -> None:
        if os.path.isfile(text_path):
            os.remove(text_path)
        if os.path.isfile(output_path):
            os.remove(output_path)

    def __make_temp_text_path(self, uuid: int, top_title: str) -> str:
        text_path: str = Config.text_path() + f"/{uuid}.txt"

        self.__make_dir_if_not_exists(text_path)

        with open(text_path, "w+t") as file:
            file.write(top_title)
        return text_path

    def __make_temp_output_path(self, uuid: int) -> str:
        output_path: str = Config.output_path() + f"/{uuid}.mp4"

        self.__make_dir_if_not_exists(output_path)

        return output_path

    @staticmethod
    def __make_dir_if_not_exists(path: str) -> None:
        dir_name: AnyStr = os.path.dirname(path)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)