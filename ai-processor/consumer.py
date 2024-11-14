import json
import logging

import pika
from pika.channel import Channel
from pika.spec import BasicProperties
from pika.spec import Basic

from gpt_processor import create_shorts_title_gpt, EditPoint, create_shorts_edit_point
from request_dto import Subtitle
from result_sender import send_fail, send_success
from utils import make_subscription


__QUEUE_IP = "54.180.140.202"
__QUEUE_NAME = "ai-process"

logging.basicConfig(level=logging.INFO)
__logger = logging.getLogger("consumer")
__logger.setLevel(logging.INFO)


def callback(ch: Channel,
             method: Basic.Deliver,
             properties: BasicProperties,
             body: bytes) -> None:
    try:
        data: dict = json.loads(body.decode('utf-8'))
        draft_id: int = data['draftId']
        input_list = data['subtitleList']

        subtitle_list: list[Subtitle] = []

        for inp in input_list:
            start: int = inp['start']
            end: int = inp['end']
            subtitle: str = inp['subtitle']
            subtitle_list.append(Subtitle(start, end, subtitle))

        __logger.info(f"draftId : {draft_id}")
        __logger.info(f"subtitleList : {subtitle_list}")

        subscription: str = make_subscription(subtitle_list)
        title: str = create_shorts_title_gpt(subscription)
        edit_point: EditPoint = create_shorts_edit_point(subscription)

        __logger.info("finished")
        __logger.info(f"title: {title} / start: {edit_point.start} / end: {edit_point.end}")

    except Exception as e:
        __logger.error(e)
        send_fail(str(e))
    else:
        send_success(draft_id=draft_id, title=title, edit_point=edit_point)
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(__QUEUE_IP, heartbeat=60))
    channel = connection.channel()

    channel.queue_declare(queue=__QUEUE_NAME)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=__QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    channel.start_consuming()




