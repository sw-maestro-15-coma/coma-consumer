import subprocess

from config import Config
from domain.id_generator import IdGenerator
from domain.shorts_thumbnail_maker import ShortsThumbnailMaker

class FfmpegShortsThumbnailMaker(ShortsThumbnailMaker):
    def execute(self, shorts_path: str) -> str:
        uuid: int = IdGenerator.make_id()

        output_path: str = Config.thumbnail_path() + f"/{uuid}.png"

        result = subprocess.run(args=self.__get_command(shorts_path=shorts_path, output_path=output_path),
                                    capture_output=True)

        if result.returncode != 0:
            raise RuntimeError("shorts 생성에 실패했습니다 : 에러 코드 - " + f"{result.returncode}")
        return output_path

    @staticmethod
    def __get_command(shorts_path: str, output_path: str) -> list[str]:
        return [
            'ffmpeg',
            '-i',
            shorts_path,
            '-ss',
             '00:00:00',
            '-frames:v',
            '1',
            '-update',
            '1',
            output_path
        ]
