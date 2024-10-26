import recv, os
import logging
from threading import Thread
from dotenv import load_dotenv

import uvicorn
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

def start():
    logger.info('Starting "youtube-downloader" consumer...')
    load_dotenv()
    host = os.environ.get('HOST')
    while True:
        try:
            recv.consume(host)
        except Exception as e:
            logger.error(f"에러 발생: {e}")

app = FastAPI()

@app.get("/healthcheck")
def health_check():
    return {"message": "ok"}

if __name__ == "__main__":
    consumer_thread = Thread(target=start)
    consumer_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)