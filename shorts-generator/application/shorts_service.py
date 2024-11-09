import os

from domain.file_system import FileSystem
from domain.time_formatter import TimeFormatter
from domain.shorts_processor import ShortsProcessor
from domain.shorts_repository import ShortsRepository
from domain.shorts_thumbnail_maker import ShortsThumbnailMaker
from domain.subtitle_file_maker import SubtitleFileMaker
from domain.temp_text_file import TempTextFile
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage


class InputFiles:
    def __init__(self, text_path: str, subtitle_path: str, input_path: str) -> None:
        self.text_path = text_path
        self.subtitle_path = subtitle_path
        self.input_path = input_path


class ShortsService:
    def __init__(self,
                 shorts_processor: ShortsProcessor,
                 shorts_repository: ShortsRepository,
                 shorts_thumbnail_maker: ShortsThumbnailMaker,
                 file_system: FileSystem,
                 subtitle_file_maker: SubtitleFileMaker) -> None:
        self.__shorts_processor = shorts_processor
        self.__shorts_repository = shorts_repository
        self.__shorts_thumbnail_maker = shorts_thumbnail_maker
        self.__file_system = file_system
        self.__subtitle_file_maker = subtitle_file_maker


    def make_shorts(self, message: ShortsRequestMessage) -> ShortsResponseMessage:
        input_files: InputFiles = self.__make_inputs(message)

        output_path: str = self.__shorts_processor.execute(s3_url=message.video_s3_url,
                                                           input_path=input_files.input_path,
                                                           text_path=input_files.text_path,
                                                           subtitle_path=input_files.subtitle_path,
                                                           start=TimeFormatter.convert_to_hhmmss(message.start_time),
                                                           end=TimeFormatter.convert_to_hhmmss(message.end_time))
        thumbnail_path: str = self.__shorts_thumbnail_maker.execute(shorts_path=output_path)

        shorts_link: str = self.__shorts_repository.post_shorts(output_path=output_path)
        thumbnail_link: str = self.__shorts_repository.post_thumbnail(thumbnail_path=thumbnail_path)

        self.__file_system.remove_all_temp_files([input_files.text_path,
                                                  output_path,
                                                  thumbnail_path,
                                                  input_files.subtitle_path,
                                                  input_files.input_path])

        return ShortsResponseMessage(shorts_id=message.shorts_id,
                                     shorts_link=shorts_link,
                                     thumbnail_link=thumbnail_link)


    def __make_inputs(self, message: ShortsRequestMessage) -> InputFiles:
        temp_text_file = TempTextFile(self.__file_system)
        temp_text_file.write_to_file(self.__add_next_line_if_over_10(message.top_title))
        text_path: str = temp_text_file.get_text_path()

        subtitle_path: str = self.__subtitle_file_maker.make_subtitle_file(message.subtitle_list)

        input_path: str = self.__shorts_repository.download_shorts(message.video_s3_url)

        return InputFiles(text_path, subtitle_path, input_path)


    def __add_next_line_if_over_10(self, title: str) -> str:
        if len(title) <= 10:
            return title

        full_length: int = len(title)

        first: str = title[:full_length // 2]
        second: str = title[full_length // 2:]

        return first + '\n' + second
