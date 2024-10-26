import pika, json
import utils
import logging
import json


logger = logging.getLogger("queue-consumer")
logger.setLevel(logging.INFO)

bucket_name = 'video-process-bucket'

class DataKeyNotFoundException(Exception):
    pass

def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode('utf-8'))
        for key, value in data.items():
            logger.info(f"{key}: {value}")

        video_id = data.get('videoId')
        youtube_url = data.get('youtubeUrl')

        if youtube_url and video_id:
            video_title = utils.get_video_title(youtube_url)
            logger.info(f"video title: {video_title}")

            youtube_key = youtube_url.split('=')[-1]
            file_name = utils.youtube_download(youtube_url)
            logger.info(f"video downloaded: {file_name}")

            duration = utils.get_duration(file_name)
            logger.info(f"video duration: {duration}")

            s3_key = f'origin/{youtube_key}.{file_name.split(".")[-1]}'
            utils.upload_to_s3(file_name, bucket_name, s3_key)
            logger.info(f"video uploaded to s3://{bucket_name}/{s3_key}")
        else:
            raise DataKeyNotFoundException()

    except DataKeyNotFoundException as e:
        logger.error(f"key not found: {data}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"callback error: {e}")
        body = {
            "videoId": video_id,
            "error": str(e)
        }
        utils.post_fail_to_api(body)
        raise e

    else:
        body = {
            "videoId": video_id,
            "s3Url": f"s3://{bucket_name}/{s3_key}",
            "videoFullSecond": duration,
            "originalTitle": video_title
        }
        utils.post_success_to_api(body)
        logger.info(f"video info sent to api")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def consume(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    logger.info('Connected to RabbitMQ')

    channel.queue_declare(queue='video-download')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='video-download', on_message_callback=callback, auto_ack=False)
    logger.info('Waiting for messages...')
    channel.start_consuming()
