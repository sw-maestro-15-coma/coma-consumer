import os
from typing import AnyStr

from config import Config
from domain.file_system import FileSystem
from domain.id_generator import IdGenerator
from domain.time_formatter import TimeFormatter
from dto.subtitle import Subtitle


class SubtitleFileMaker:
    def __init__(self, file_system: FileSystem) -> None:
        self.__file_system = file_system


    def make_subtitle_file(self, subtitle_list: list[Subtitle])-> str:
        uuid: int = IdGenerator.make_id()
        temp_path: str = Config.subtitle_path() + f"/{uuid}.srt"

        dir_name: str = self.__file_system.extract_dir_name(temp_path)
        self.__file_system.make_dir_if_not_exists(dir_name)

        self.__file_system.write_text_to_file(file_path=temp_path,
                                              content=self.__make_srt_format(subtitle_list))

        return temp_path


    def __make_srt_format(self, subtitles: list[Subtitle]) -> str:
        result: str = ""
        cnt: int = 1

        for subtitle in subtitles:
            start_time: str = TimeFormatter.convert_to_hhmmss_mmm(subtitle.start)
            end_time: str = TimeFormatter.convert_to_hhmmss_mmm(subtitle.end)

            result += f"{cnt}\n"
            result += f"{start_time} --> {end_time}\n"
            result += f"{subtitle.subtitle}\n"
            result += "\n"
            cnt += 1

        return result