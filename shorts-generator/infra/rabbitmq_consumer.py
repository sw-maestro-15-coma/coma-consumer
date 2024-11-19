import json
import logging
import time

import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel

from application.shorts_service import ShortsService
from config import Config
from domain.shorts_result_sender import ShortsResultSender
from dto.shorts_request_message import ShortsRequestMessage
from dto.shorts_response_message import ShortsResponseMessage
from dto.subtitle import Subtitle


class RabbitMQConsumer:
    def __init__(self,
                 shorts_service: ShortsService,
                 shorts_result_sender: ShortsResultSender) -> None:
        self.shorts_service = shorts_service
        self.shorts_result_sender = shorts_result_sender


    def start(self) -> None:
        def callback(ch: BlockingChannel, method, properties, body):
            try:
                data: dict = json.loads(body.decode('utf-8'))

                logging.info("메시지 수신")

                for key, value in data.items():
                    logging.info(f"[shorts_processor] {key}: {value}")

                subtitle_list: list[Subtitle] = []

                for sub in data['subtitleList']:
                    temp = Subtitle(int(sub['start']), int(sub['end']), sub['subtitle'])
                    subtitle_list.append(temp)

                message = ShortsRequestMessage(shorts_id=data['shortsId'],
                                               video_s3_url=data['videoS3Url'],
                                               top_title=data['topTitle'],
                                               start_time=data['startTime'],
                                               end_time=data['endTime'],
                                               subtitle_list=subtitle_list)

                response: ShortsResponseMessage = self.shorts_service.make_shorts(message)
            except Exception as e:
                logging.error("shorts 생성 실패")
                logging.error(e)
                self.shorts_result_sender.send_fail(str(e), shorts_id=data['shortsId'])

            else:
                logging.info("shorts 생성 성공")
                self.shorts_result_sender.send_success(response)

        while True:
            try:
                connection: BlockingConnection = pika.BlockingConnection(pika.ConnectionParameters("54.180.140.202", heartbeat=600))
                channel: BlockingChannel = connection.channel()
                channel.queue_declare(queue=Config.queue_name())

                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=Config.queue_name(), on_message_callback=callback, auto_ack=True)

                channel.start_consuming()
            except Exception as e:
                logging.error(e)
