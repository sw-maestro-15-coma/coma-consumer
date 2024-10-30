import json

import requests

from gpt_processor import EditPoint


__API_SERVER_URL = "https://api.cotuber.com/api/v1/message"


def send_success(draft_id: int, title: str, edit_point: EditPoint) -> None:
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "draftId": draft_id,
        "title": title,
        "start": edit_point.start,
        "end": edit_point.end
    }
    requests.post(__API_SERVER_URL + "/ai", data=json.dumps(data), headers=headers)


def send_fail(error_message)-> None:
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "shortsId": 0,
        "message": error_message
    }
    requests.post(__API_SERVER_URL + "/fail", data=json.dumps(data), headers=headers)