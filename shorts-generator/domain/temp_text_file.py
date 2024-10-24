import os
from typing import AnyStr

from config import Config
from domain.id_generator import IdGenerator


class TempTextFile:
    def __init__(self) -> None:
        uuid: int = IdGenerator.make_id()
        self.__text_file_path: str = Config.text_path() + f"/{uuid}.txt"

    def get_text_path(self):
        return self.__text_file_path

    def write_to_file(self, top_title: str) -> None:
        self.__make_dir_if_not_exists()

        with open(self.__text_file_path, "w+t") as file:
            file.write(top_title)

    def __make_dir_if_not_exists(self) -> None:
        self.__check_null()
        dir_name: AnyStr = os.path.dirname(self.__text_file_path)

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    def __check_null(self):
        if not self.__text_file_path:
            raise RuntimeError("텍스트 파일을 지정해야합니다")