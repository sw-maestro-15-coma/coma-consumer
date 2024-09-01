
class Config:
    __state: str = "test"

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
        return "https://api.cotuber.com/api/v1/message/"

    @staticmethod
    def s3_bucket_name() -> str:
        return "video-process-test-bucket"

    @staticmethod
    def queue_name() -> str:
        return "shorts-process"

    @classmethod
    def font_path(cls) -> str:
        if cls.__state == "test":
            return "/Users/choejaewon/Desktop/projects/coma-consumer-clone/coma-consumer/shorts-generator/extrabold.ttf"
        return "/usr/share/fonts/truetype/extrabold.ttf"

    @staticmethod
    def s3_url() -> str:
        return "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/"

    @classmethod
    def text_path(cls) -> str:
        if cls.__state == "test":
            return "/Users/choejaewon/Desktop/text"
        return "/text"

    @classmethod
    def output_path(cls) -> str:
        if cls.__state == "test":
            return "/Users/choejaewon/Desktop/output"
        return "/output"
