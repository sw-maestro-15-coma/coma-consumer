from fastapi import FastAPI

from video import router

app = FastAPI()

app.include_router(router)


@app.get("/health-check")
def health_check():
    return {"message": "ok"}
