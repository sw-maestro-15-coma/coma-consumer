from fastapi import FastAPI
from threading import Thread
import uvicorn
import pika
import logging
import requests
from pika.adapters.blocking_connection import BlockingChannel

from rearrange_subtitle import SubtitleReconstructor
from subtitle import SubtitleResult
from whisper_subtitle_generator import subtitle_generator
from s3 import download_video, delete_video
from convert_audio import convert_audio, delete_audio
from kiwi_sentence_end_checker import sentence_end_checker

import json

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.get("/generate-subtitles", summary="테스트를 위한 api")
def generate_subtitles_endpoint(video_id: int, s3_url: str):
    subtitles = logic(video_id, s3_url)
    return subtitles


def logic(video_id: int, s3_url: str) -> SubtitleResult:
    video_path = download_video(video_id, s3_url)
    audio_path = convert_audio(video_id, video_path)
    delete_video(video_path)

    subtitle = subtitle_generator.generate_subtitle(audio_path)
    delete_audio(audio_path)

    rearrange_subtitle = SubtitleReconstructor(sentence_end_checker).reconstruct(subtitle.subtitles)

    return rearrange_subtitle


def send_success(videoId: int, subtitle: SubtitleResult):
    headers = {'Content-Type': 'application/json; charset;utf-8'}
    data = {
        "videoId": videoId,
        "subtitleList": list(map(lambda x: x.__dict__, subtitle.subtitles))
    }
    requests.post("https://api.cotuber.com/api/v1/message/subtitle", data=json.dumps(data), headers=headers)


def send_fail(message: str, video_id: int):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "videoId": video_id,
        "message": message
    }
    requests.post("https://api.cotuber.com/api/v1/message/subtitle/fail", data=json.dumps(data), headers=headers)


def start():
    def callback(ch: BlockingChannel, method, properties, body):
        data: dict = json.loads(body.decode('utf-8'))

        logging.info("메시지 수신")

        for key, value in data.items():
            print(f"[subtitle-generate] {key}: {value}")

        try:
            response: SubtitleResult = logic(data['videoId'], data['s3Url'])
        except Exception as e:
            logging.error("shorts 생성 실패")
            print(e)
            logging.error(e)
            send_fail("쇼츠 생성에 실패했습니다", video_id=data['videoId'])
            # raise e
        else:
            logging.info("shorts 생성 성공")
            send_success(data['videoId'], response)

    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("54.180.140.202", heartbeat=1200))
            channel: BlockingChannel = connection.channel()
            channel.queue_declare(queue='video-subtitle-generate')

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='video-subtitle-generate', on_message_callback=callback, auto_ack=True)

            channel.start_consuming()
        except Exception as e:
            logging.error("rabbitmq 연결 실패")
            logging.error(e)


if __name__ == "__main__":
    consumer_thread = Thread(target=start)
    consumer_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
