from config import Config
from domain.id_generator import IdGenerator
from domain.shorts_processor import ShortsProcessor
from domain.shorts_repository import ShortsRepository
from domain.temp_files import TempFiles
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

        temp_files: TempFiles = TempFiles(uuid= uuid,
                                          top_title=message.top_title)
        text_path: str = temp_files.get_text_path()
        output_path: str = temp_files.get_output_path()

        self.shorts_processor.execute(self.__message_to_request(message,
                                                                text_path=text_path,
                                                                output_path=output_path))
        self.shorts_repository.post_shorts(output_path=output_path, file_name=f"{uuid}.mp4")

        temp_files.remove()

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
