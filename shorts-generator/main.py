import logging

from fastapi import FastAPI

from dto.shorts_request_message import ShortsRequestMessage
from dto.subtitle import Subtitle
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
        video_s3_url="https://video-process-test-bucket.s3.ap-northeast-2.amazonaws.com/origin/599903428704431693.webm",
        top_title="테스트 제목입니다 반갑습니다",
        start_time=0,
        end_time=30,
        subtitle_list=[
            Subtitle(0, 10, "안녕"),
            Subtitle(10, 30, "하세요")
        ]
    )

    response = shorts_service.make_shorts(message)

    logger.info(f"shorts link: {response.s3Url}")
    logger.info(f"thumbnail link : {response.thumbnailUrl}")


app = FastAPI()

@app.get("/healthcheck")
def health_check():
    return {"message": "ok"}

if __name__ == '__main__':
    start()