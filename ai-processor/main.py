import time
from threading import Thread

import uvicorn
from fastapi import FastAPI, HTTPException

from consumer import start_consume


app: FastAPI = FastAPI()


@app.get("/healthcheck")
def health_check():
    return {
        "message": "ok"
    }


if __name__ == '__main__':
    consumer_thread = Thread(target=start_consume)
    consumer_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)