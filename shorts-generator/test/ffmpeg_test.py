import os.path
import unittest

from urllib3 import request

from config import Config
from domain.shorts_processor import ShortsProcessor
from dto.shorts_request import ShortsRequest
from dto.shorts_request_message import ShortsRequestMessage
from main import start
from object_factory import ObjectFactory


class FfmpegTest(unittest.TestCase):
    __VALID_S3_URL = "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/origin/599903428704431693.webm"
    shorts_processor: ShortsProcessor = ObjectFactory.shorts_processor()

    def test_invalid_s3_url(self):
        shorts_request = ShortsRequest(s3_url="abc.com",
                                       text_path="/",
                                       output_path="/",
                                       start="00:00:00",
                                       end="00:00:00")

        with self.assertRaises(RuntimeError):
            self.shorts_processor.execute(request=shorts_request)

    def test_invalid_start(self):
        shorts_request: ShortsRequest = ShortsRequest(s3_url=self.__VALID_S3_URL,
                                                      text_path="/text/some.txt",
                                                      output_path="/output/some.mp4",
                                                      start="abc",
                                                      end="00:01:00")
        with self.assertRaises(RuntimeError):
            self.shorts_processor.execute(request=shorts_request)

    def test_process_success(self):
        output_path: str = Config.output_path() + "/test.mp4"
        text_path: str = Config.text_path() + "/test.txt"
        with open(text_path, 'w+') as file:
            file.write("테스트 제목")

        shorts_request: ShortsRequest = ShortsRequest(s3_url=self.__VALID_S3_URL,
                                                      text_path=text_path,
                                                      output_path=output_path,
                                                      start="00:01:00",
                                                      end="00:02:00")

        self.shorts_processor.execute(shorts_request)
        result: bool = os.path.getsize(output_path) > 0

        self.assertTrue(result)
        if os.path.isfile(text_path):
            os.remove(text_path)
        if os.path.isfile(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    unittest.main()