import logging

from dto.shorts_request_message import ShortsRequestMessage
from object_factory import ObjectFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

def start():
    consumer = ObjectFactory.rabbitmq_consumer()
    logger.info("시작 성공")
    consumer.start()

def test_start():
    shorts_service = ObjectFactory.shorts_service()
    message = ShortsRequestMessage(
        shorts_id=0,
        video_id=0,
        video_s3_url="https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/origin/599903428704431693.webm",
        top_title="테스트 제목입니다 반갑습니다",
        start_time="00:05:00",
        end_time="00:06:00"
    )

    response = shorts_service.make_shorts(message)

    logger.info(f"shorts link: {response.shorts_link}")
    logger.info(f"thumbnail link : {response.thumbnail_link}")

if __name__ == '__main__':
    test_start()