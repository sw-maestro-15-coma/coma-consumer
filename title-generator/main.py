import uvicorn
from fastapi import FastAPI, HTTPException

from request_dto import RequestDto, Subtitle
from gpt_processor import create_shorts_title_gpt, EditPoint, create_shorts_edit_point
from utils import make_subscription


app: FastAPI = FastAPI()


@app.post("/ai/title")
def generate_title(request_body: RequestDto):
    try:
        title: str = create_shorts_title_gpt(subscription=make_subscription(request_body.subtitleList))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)

    return {
        "title": title,
        "draftId": request_body.draftId
    }


@app.post("/ai/edit")
def generate_edit_point(request_body: RequestDto):
    try:
        edit_point: EditPoint = create_shorts_edit_point(subscription=make_subscription(request_body.subtitleList))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)

    return {
        "start": edit_point.start,
        "end": edit_point.end
    }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)