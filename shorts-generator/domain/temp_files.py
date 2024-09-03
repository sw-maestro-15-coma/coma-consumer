import os
from typing import AnyStr

from config import Config


class TempFiles:
    def __init__(self, uuid: int, top_title: str) -> None:
        self.__check_null(top_title)

        try:
            self.__text_path: str = self.__make_temp_text_path(uuid=uuid, top_title=top_title)
            self.__output_path: str = self.__make_temp_output_path(uuid)
        except Exception as e:
            raise RuntimeError(e)

    def get_text_path(self) -> str:
        return self.__text_path

    def get_output_path(self) -> str:
        return self.__output_path

    def remove(self) -> None:
        try:
            if os.path.isfile(self.__text_path):
                os.remove(self.__text_path)
            if os.path.isfile(self.__output_path):
                os.remove(self.__output_path)
        except Exception as e:
            raise RuntimeError(e)

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

    @staticmethod
    def __check_null(top_title: str) -> None:
        if top_title is None:
            raise RuntimeError("top title이 null입니다")