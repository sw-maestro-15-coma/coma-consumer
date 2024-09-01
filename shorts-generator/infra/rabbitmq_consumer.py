import json
import logging

import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel

from application.shorts_service import ShortsService
from config import Config
from domain.shorts_result_sender import ShortsResultSender
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage

class RabbitMQConsumer:
    def __init__(self,
                 shorts_service: ShortsService,
                 shorts_result_sender: ShortsResultSender) -> None:
        self.shorts_service = shorts_service
        self.shorts_result_sender = shorts_result_sender

    def start(self) -> None:
        connection: BlockingConnection = pika.BlockingConnection(pika.ConnectionParameters("54.180.140.202"))
        channel: BlockingChannel = connection.channel()
        channel.queue_declare(queue=Config.queue_name())

        def callback(ch: BlockingChannel, method, properties, body):
            data: dict = json.loads(body.decode('utf-8'))

            logging.info("메시지 수신")

            for key, value in data.items():
                logging.info(f"[shorts_processor] {key}: {value}")

            message = ShortsRequestMessage(video_id=data['videoId'],
                                           video_s3_url=['videoS3Url'],
                                           shorts_id=data['shortsId'],
                                           top_title=data['topTitle'],
                                           start_time=data['startTime'],
                                           end_time=data['endTime'])

            try:
                response: ShortsResponseMessage = self.shorts_service.make_shorts(message)
            except Exception as e:
                logging.error("shorts 생성 실패")
                self.shorts_result_sender.send_fail("쇼츠 생성에 실패했습니다", shorts_id=data['shortsId'])
                raise e
            else:
                logging.info("shorts 생성 성공")
                self.shorts_result_sender.send_success(response)
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=Config.queue_name(), on_message_callback=callback, auto_ack=False)

        channel.start_consuming()
