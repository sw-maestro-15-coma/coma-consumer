from fastapi import FastAPI
from threading import Thread
import uvicorn
import pika

from whisper_subtitle_generator import subtitle_generator
from s3 import download_video
from convert_audio import convert_audio

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}


@app.get("/generate-subtitles", summary="테스트를 위한 api")
def generate_subtitles_endpoint(video_id: int, s3_url: str):
    subtitles = logic(video_id, s3_url)
    return subtitles


def logic(video_id: int, s3_url: str):
    video_path = download_video(video_id, s3_url)
    audio_path = convert_audio(video_id, video_path)

    return subtitle_generator.generate_subtitle(audio_path)


# def rabbitmq_callback(ch, method, properties, body):
#     # 요청 처리
#     video_s3_url = body.decode('utf-8')
#     process_video_from_s3(video_s3_url)
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#
#
# def start_rabbitmq_consumer():
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()
#     channel.queue_declare(queue='video_queue')
#
#     channel.basic_consume(queue='video_queue', on_message_callback=rabbitmq_callback)
#     print('메시지를 기다리는 중입니다. 종료하려면 CTRL+C를 누르세요.')
#     channel.start_consuming()


if __name__ == "__main__":
    # consumer_thread = Thread(target=start_rabbitmq_consumer)
    # consumer_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
