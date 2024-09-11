import subprocess

from config import Config
from domain.id_generator import IdGenerator
from domain.shorts_processor import ShortsProcessor
from dto.shorts_request import ShortsRequest

class FfmpegShortsProcessor(ShortsProcessor):
    __FONT_PATH = Config.font_path()

    def execute(self, request: ShortsRequest) -> str:
        uuid: int = IdGenerator.make_id()
        output_path: str = Config.output_path() + f"/{uuid}.mp4"

        result = subprocess.run(args=self.__get_command(request, output_path),
                                capture_output=True)

        if result.returncode != 0:
            raise RuntimeError("shorts 생성에 실패했습니다 : 에러 코드 - " + f"{result.returncode}")

        return output_path


    def __get_command(self, request: ShortsRequest, output_path: str) -> list[str]:
        return [
            'ffmpeg',
            '-i',
            request.s3_url,
            '-vf',
            self.__get_video_filter(request.text_path),
            '-ss',
            request.start,
            '-to',
            request.end,
            '-f',
            'mp4',
            '-y',
            output_path
        ]

    def __get_video_filter(self, text_path: str) -> str:
        return ("scale=1080:1920:force_original_aspect_ratio=decrease,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2," +
                f"drawtext=textfile={text_path}:fontfile={self.__FONT_PATH}" 
                ":fontcolor=white:fontsize=100:x=(w-text_w)/2:y=200")