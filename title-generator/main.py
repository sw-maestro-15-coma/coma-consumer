import uvicorn
from fastapi import FastAPI, HTTPException

from request_dto import RequestDto, Subtitle
from gpt_processor import create_shorts_title_gpt, EditPoint, create_shorts_edit_point

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


@app.post("/ai/edit")
def generate_edit_point(request_body: RequestDto):
    try:
        edit_point: EditPoint = create_shorts_edit_point(subscription=__make_subscription(request_body.subtitleList))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)

    return {
        "start": edit_point.start,
        "end": edit_point.end
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


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)