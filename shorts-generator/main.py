import logging
from threading import Thread

import uvicorn
from fastapi import FastAPI

from object_factory import ObjectFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


def start():
    consumer = ObjectFactory.rabbitmq_consumer()
    logger.info("시작 성공")
    consumer.start()


app = FastAPI()


@app.get("/healthcheck")
def health_check():
    return {"message": "ok"}


if __name__ == '__main__':
    consumer_thread = Thread(target=start)
    consumer_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)