from fastapi import FastAPI

from ..app.video import router

app = FastAPI()

app.include_router(router)


@app.get("/health-check")
def health_check():
    return {"message": "ok"}
