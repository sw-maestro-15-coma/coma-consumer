import json

import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from pika.channel import Channel
from pika.spec import Basic, BasicProperties

from main import upload_to_youtube
from result_sender import send_result

__QUEUE_IP = "54.180.140.202"
__QUEUE_NAME = "youtube-upload"

def callback(ch: Channel,
             method: Basic.Deliver,
             properties: BasicProperties,
             body: bytes) -> None:
    data: dict = json.loads(body.decode("utf-8"))

    shorts_url: str = data['shorts_url']
    access_token: str = data['access_token']
    title: str = data['title']
    description: str = data['description']

    try:
        upload_to_youtube(access_token=access_token,
                          title=title,
                          description=description,
                          file_path=get_shorts_file_path(shorts_url))
    except Exception as e:
        send_result("fail", e)
    else:
        send_result("SUCCESS", "SUCCESS")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consume() -> None:
    connection: BlockingConnection = pika.BlockingConnection(pika.ConnectionParameters(__QUEUE_IP))
    channel: BlockingChannel = connection.channel()

    channel.queue_declare(queue=__QUEUE_NAME)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=__QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    channel.start_consuming()


def get_shorts_file_path(shorts_url: str) -> str:
    return ""