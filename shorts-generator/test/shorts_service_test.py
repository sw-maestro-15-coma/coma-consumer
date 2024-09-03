import unittest
from os.path import pathsep
from unittest.mock import Mock, patch

from application.shorts_service import ShortsService
from config import Config
from domain.id_generator import IdGenerator
from domain.shorts_processor import ShortsProcessor
from domain.shorts_repository import ShortsRepository
from domain.temp_files import TempFiles
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage

class ShortsServiceTest(unittest.TestCase):
    __S3_URL = Config.s3_url()
    mock_shorts_processor: ShortsProcessor = Mock()
    mock_shorts_repository: ShortsRepository = Mock()
    mock_shorts_id_generator: IdGenerator = Mock()

    @patch("application.shorts_service.TempFiles")
    def test_success(self, MockTempFiles) -> None:
        self.mock_shorts_id_generator.make_id.return_value = 1234
        MockTempFiles.mock_temp_files.remove.return_value = None
        MockTempFiles.mock_temp_files.get_text_path.return_value = "/text/1234.txt"
        MockTempFiles.mock_temp_files.get_output_path.return_value = "/output/1234.txt"

        shorts_service = ShortsService(
            shorts_processor=self.mock_shorts_processor,
            shorts_repository=self.mock_shorts_repository,
            id_generator=self.mock_shorts_id_generator
        )

        message: ShortsRequestMessage = ShortsRequestMessage(
            shorts_id=0,
            video_id=0,
            video_s3_url="abc.com",
            top_title="top_title",
            start_time="00:01:00",
            end_time="00:02:00"
        )
        response: ShortsResponseMessage = shorts_service.make_shorts(message)

        self.assertEqual(response.link, self.__S3_URL + "process/1234.mp4")
        self.mock_shorts_repository.post_shorts.assert_called_once()

    def test_fail_on_processor(self) -> None:
        self.mock_shorts_processor.execute.side_effect=Exception("processor 오류 발생")

        shorts_service: ShortsService = ShortsService(
            shorts_processor=self.mock_shorts_processor,
            shorts_repository=self.mock_shorts_repository,
            id_generator=self.mock_shorts_id_generator
        )
        with self.assertRaises(Exception):
            shorts_service.make_shorts(None)


if __name__ == '__main__':
    unittest.main()
