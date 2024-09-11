import subprocess

from domain.shorts_thumbnail_maker import ShortsThumbnailMaker

class FfmpegShortsThumbnailMaker(ShortsThumbnailMaker):
    def execute(self, shorts_link: str) -> str:
        __FONT_PATH = Config.font_path()


        print(self.__get_command(request=request))

        result = subprocess.run(args=self.__get_command(request),
                                    capture_output=True)

        if result.returncode != 0:
            raise RuntimeError("shorts 생성에 실패했습니다")

    def __get_command(self, shorts_path: str, thumbnail_path: str) -> list[str]:
        return [
                'ffmpeg',
                '-i',
                shorts_path
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
