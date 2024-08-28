import unittest

from application.shorts_service import ShortsService
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage
from object_factory import ObjectFactory

class MyTestCase(unittest.TestCase):
    def test_work(self):
        shorts_service: ShortsService = ObjectFactory.shorts_service()

        video_id = 0
        shorts_id = 0
        top_title = "테스트 제목입니다"
        video_s3_url = "https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/origin/600573444141835878.webm"
        start_time = "00:01:00"
        end_time = "00:02:00"
        shorts_request_message: ShortsRequestMessage = ShortsRequestMessage(
            video_id=video_id,
            shorts_id=shorts_id,
            top_title=top_title,
            video_s3_url=video_s3_url,
            start_time=start_time,
            end_time=end_time
        )
        response: ShortsResponseMessage = shorts_service.make_shorts(shorts_request_message)

        print(response.link)

if __name__ == '__main__':
    unittest.main()
