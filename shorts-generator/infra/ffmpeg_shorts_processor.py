import subprocess

from config import Config
from domain.shorts_processor import ShortsProcessor
from dto.shorts_request import ShortsRequest

class FfmpegShortsProcessor(ShortsProcessor):
    __FONT_PATH = Config.font_path()

    def execute(self, request: ShortsRequest) -> None:
        print(self.__get_command(request=request))

        result = subprocess.run(args=self.__get_command(request),
                                capture_output=True)

        if result.returncode != 0:
            raise RuntimeError("shorts 생성에 실패했습니다")

    def __get_command(self, request: ShortsRequest) -> list[str]:
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
            request.output_path
        ]

    def __get_video_filter(self, text_path: str) -> str:
        return ("scale=1080:1920:force_original_aspect_ratio=decrease,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2," +
                f"drawtext=textfile={text_path}:fontfile={self.__FONT_PATH}" 
                ":fontcolor=white:fontsize=100:x=(w-text_w)/2:y=200")