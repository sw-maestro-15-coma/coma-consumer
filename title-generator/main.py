from fastapi import FastAPI

from request_dto import RequestDto, Subtitle
from title_generator import create_shorts_title_gpt


app: FastAPI = FastAPI()

@app.post("/ai/title")
def generate_title(request_body: RequestDto):
    title: str = create_shorts_title_gpt(subscription=__make_subscription(request_body.subtitleList))

    return {"title": title}

def __make_subscription(subtitles: list[Subtitle]) -> str:
    result: str = ""

    for sub in subtitles:
        result += f"{sub.start} ~ {sub.end}\n"
        result += f"{sub.subtitle}\n"
        result += "\n"

    return result