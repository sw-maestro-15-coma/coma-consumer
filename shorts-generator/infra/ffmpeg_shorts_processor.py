import subprocess

from config import Config
from domain.id_generator import IdGenerator
from domain.shorts_processor import ShortsProcessor

class FfmpegShortsProcessor(ShortsProcessor):
    __FONT_PATH = Config.font_path()

    def execute(self,
                s3_url: str,
                input_path: str,
                text_path: str,
                start: str,
                end: str,
                subtitle_path: str) -> str:
        uuid: int = IdGenerator.make_id()
        output_path: str = Config.output_path() + f"/{uuid}.mp4"

        result = subprocess.run(args=self.__get_command(s3_url=s3_url,
                                                        input_path=input_path,
                                                        text_path=text_path,
                                                        start=start,
                                                        end=end,
                                                        output_path=output_path,
                                                        subtitle_path=subtitle_path),
                                capture_output=True)

        if result.returncode != 0:
            raise RuntimeError("shorts 생성에 실패했습니다 : 에러 코드 - " + f"{result.returncode}")

        return output_path


    def __get_command(self,
                      s3_url: str,
                      input_path: str,
                      text_path: str,
                      start: str,
                      end: str,
                      output_path: str,
                      subtitle_path: str) -> list[str]:
        return [
            'ffmpeg',
            '-i',
            input_path,
            '-vf',
            self.__get_video_filter(text_path, subtitle_path),
            '-ss',
            start,
            '-to',
            end,
            '-f',
            'mp4',
            '-y',
            output_path
        ]


    def __get_video_filter(self, text_path: str, subtitle_path: str) -> str:
        return ("scale=1080:1920:force_original_aspect_ratio=decrease,setsar=1:1,"
                "pad=1080:1920:(ow-iw)/2:(oh-ih)/2,scale=iw*1.5:ih*1.5,crop=1080:1920" +
                f"drawtext=textfile={text_path}:fontfile={self.__FONT_PATH}" 
                ":fontcolor=white:fontsize=100:x=(w-text_w)/2:y=200,"
                f"subtitles={subtitle_path}")