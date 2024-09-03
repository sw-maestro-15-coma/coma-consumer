import logging

from object_factory import ObjectFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

def start():
    consumer = ObjectFactory.rabbitmq_consumer()
    logger.info("시작 성공")
    consumer.start()

if __name__ == '__main__':
    start()