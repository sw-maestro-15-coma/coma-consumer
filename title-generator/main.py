from fastapi import FastAPI, HTTPException

from request_dto import RequestDto, Subtitle
from title_generator import create_shorts_title_gpt


app: FastAPI = FastAPI()

"""
    Request Body
    {
        draftId: int,
        subtitleList: {
            start: int,
            end: int,
            subtitle: str
        } []
    }
"""
@app.post("/ai/title")
def generate_title(request_body: RequestDto):
    try:
        title: str = create_shorts_title_gpt(subscription=__make_subscription(request_body.subtitleList))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)

    return {
        "title": title,
        "draftId": request_body.draftId
    }


def __make_subscription(subtitles: list[Subtitle]) -> str:
    result: str = ""

    for sub in subtitles:
        result += f"{__second_to_hhmmss(sub.start)} ~ {__second_to_hhmmss(sub.end)}\n"
        result += f"{sub.subtitle}\n"
        result += "\n"

    return result


def __second_to_hhmmss(total_second: int) -> str:
    hour: int = total_second // 3600
    minute: int = total_second % 3600 // 60
    second: int = total_second % 60

    hh: str = __add_zero_if_length_is_one(hour)
    mm: str = __add_zero_if_length_is_one(minute)
    ss: str = __add_zero_if_length_is_one(second)

    return f"{hh}:{mm}:{ss}"


def __add_zero_if_length_is_one(time: int) -> str:
    if 0 <= time <= 9:
        return f"0{time}"
    return f"{time}"