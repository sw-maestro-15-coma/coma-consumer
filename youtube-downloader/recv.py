import pika, json, time
import utils

bucket_name = 'video-process-test-bucket'

def callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    for key, value in data.items():
        print(f"[youtube-downloader] {key}: {value}")

    youtube_url = data.get('youtubeUrl')
    if youtube_url:
        youtube_key = youtube_url.split('=')[-1]
        file_name = utils.youtube_download(youtube_url)
        print(f"[youtube-downloader] video downloaded: {file_name}")

        duration = utils.get_duration(file_name)
        print(f"[youtube-downloader] video duration: {duration}")

        s3_key = f'origin/{youtube_key}.{file_name.split(".")[-1]}'
        utils.upload_to_s3(file_name, bucket_name, s3_key)
    else:
        print(f"[youtube-downloader] youtubeUrl not found in message")

def consume(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue='youtube-downloader')

    channel.basic_consume(queue='youtube-downloader', on_message_callback=callback, auto_ack=True)

    print('[youtube-downloader] Waiting for messages...')
    channel.start_consuming()
