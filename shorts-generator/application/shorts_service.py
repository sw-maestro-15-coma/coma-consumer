import os

from domain.id_generator import IdGenerator
from domain.shorts_processor import ShortsProcessor
from domain.shorts_repository import ShortsRepository
from dto.shorts_request import ShortsRequest
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage

class ShortsService:
    __S3_URL = "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/"

    def __init__(self,
                 shorts_processor: ShortsProcessor,
                 id_generator: IdGenerator,
                 shorts_repository: ShortsRepository) -> None:
        self.shorts_processor = shorts_processor
        self.id_generator = id_generator
        self.shorts_repository = shorts_repository

    def make_shorts(self, message: ShortsRequestMessage) -> ShortsResponseMessage:
        uuid: int = self.id_generator.make_id()

        text_path = f"/text/{uuid}.txt"
        output_path = f"/output/{uuid}.mp4"

        text_file = open(text_path, 'w+t')
        text_file.write(message.top_title)
        text_file.close()

        self.shorts_processor.execute(self.__message_to_request(message,
                                                                text_path=text_path,
                                                                output_path=output_path))
        self.shorts_repository.post_shorts(output_path=output_path, file_name=f"{uuid}.mp4")


        self.__remove_temp_files(text_path=text_path,
                                 output_path=output_path)

        return ShortsResponseMessage(video_id=message.video_id,
                                     shorts_id=message.shorts_id,
                                     link=self.__S3_URL + f"{uuid}.mp4")

    def __message_to_request(self, message: ShortsRequestMessage,
                             text_path: str,
                             output_path: str) -> ShortsRequest:
        return ShortsRequest(s3_url=message.video_s3_url,
                      start=message.start_time,
                      end=message.end_time,
                      text_path=text_path,
                      output_path=output_path)

    def __remove_temp_files(self, text_path: str, output_path: str) -> None:
        if os.path.isfile(text_path):
            os.remove(text_path)
        if os.path.isfile(output_path):
            os.remove(output_path)