import json

import requests

from config import Config
from domain.shorts_result_sender import ShortsResultSender
from dto.shorts_response_message import ShortsResponseMessage

class SimpleShortsResultSender(ShortsResultSender):
    __API_SERVER_URL = Config.api_server_url()

    def send_success(self, shorts_response_message: ShortsResponseMessage) -> None:
        headers = {'Content-Type': 'application/json; charset;utf-8'}
        data = {
            'shortsId': shorts_response_message.shorts_id,
            'videoId': shorts_response_message.video_id,
            'link': shorts_response_message.link
        }
        requests.post(self.__API_SERVER_URL + "shorts", data=json.dumps(data), headers=headers)

    def send_fail(self, message: str, shorts_id: int) -> None:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
            "shortsId": shorts_id,
            "message": message
        }
        requests.post(self.__API_SERVER_URL + "fail", data=json.dumps(data), headers=headers)