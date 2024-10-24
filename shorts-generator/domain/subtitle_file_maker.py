import os
from typing import AnyStr

from config import Config
from domain.id_generator import IdGenerator
from domain.time_formatter import TimeFormatter
from dto.subtitle import Subtitle


class SubtitleFileMaker:
    @staticmethod
    def make_subtitle_file(subtitle_list: list[Subtitle])-> str:
        uuid: int = IdGenerator.make_id()
        temp_path: str = Config.subtitle_path() + f"/{uuid}.srt"

        dir_name: AnyStr = os.path.dirname(temp_path)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(temp_path, "w+t") as f:
            cnt: int = 1

            for subtitle in subtitle_list:
                start_time: str = TimeFormatter.convert_to_hhmmss_mmm(subtitle.start)
                end_time: str = TimeFormatter.convert_to_hhmmss_mmm(subtitle.end)

                f.write(f"{cnt}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.writelines(f"{subtitle.subtitle}\n")
                f.write("\n")
                cnt += 1

        return temp_path
