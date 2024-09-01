import unittest
from unittest.mock import Mock

from application.shorts_service import ShortsService
from config import Config
from dto.shorts_request import ShortsRequest
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage


class ShortsServiceTest(unittest.TestCase):
    __S3_URL = Config.s3_url()

    def test_success(self):
        mock_shorts_processor = Mock()
        mock_shorts_repository = Mock()
        mock_shorts_id_generator = Mock()

        mock_shorts_processor.execute()
        mock_shorts_repository.post_shorts()
        mock_shorts_id_generator.make_id.return_value = 1234

        shorts_service = ShortsService(
            shorts_processor=mock_shorts_processor,
            shorts_repository=mock_shorts_repository,
            id_generator=mock_shorts_id_generator
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


if __name__ == '__main__':
    unittest.main()
