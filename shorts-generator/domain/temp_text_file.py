import os
from typing import AnyStr

from config import Config
from domain.file_system import FileSystem
from domain.id_generator import IdGenerator


class TempTextFile:
    def __init__(self, file_system: FileSystem) -> None:
        uuid: int = IdGenerator.make_id()
        self.__file_system = file_system
        self.__text_file_path: str = Config.text_path() + f"/{uuid}.txt"


    def get_text_path(self):
        return self.__text_file_path


    def write_to_file(self, top_title: str) -> None:
        self.__check_null()
        dir_name: str = self.__file_system.extract_dir_name(self.__text_file_path)
        self.__file_system.make_dir_if_not_exists(dir_name)

        self.__file_system.write_text_to_file(self.__text_file_path, top_title)


    def __check_null(self):
        if not self.__text_file_path:
            raise RuntimeError("텍스트 파일을 지정해야합니다")