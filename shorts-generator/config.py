
class Config:
    @staticmethod
    def aws_access_key() -> str:
        return "AKIA6GBMEHUUKC7J7Y53"

    @staticmethod
    def aws_secret_key() -> str:
        return "ms3x60EQKnsAlG9/FK2DdchkXBrWHRCcXvr4MYKT"

    @staticmethod
    def region() -> str:
        return "ap-northeast-2"

    @staticmethod
    def api_server_url() -> str:
        return "https://api.cotuber.com/api/v1/message"

    @staticmethod
    def s3_bucket_name() -> str:
        return "video-process-test-bucket"

    @staticmethod
    def queue_name() -> str:
        return "shorts-process"

    @staticmethod
    def font_path() -> str:
        return "/usr/share/fonts/truetype/extrabold.ttf"

    @staticmethod
    def s3_url() -> str:
        return "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com"

    @staticmethod
    def text_path() -> str:
        return "/text"

    @staticmethod
    def subtitle_path() -> str:
        return "/subtitle"

    @staticmethod
    def output_path() -> str:
        return "/output"

    @staticmethod
    def thumbnail_path() -> str:
        return "/thumbnail"
