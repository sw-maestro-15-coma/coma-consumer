import pika, json
import utils

def callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    for key, value in data.items():
        print(f"[youtube-downloader] {key}: {value}")

    youtube_url = data.get('youtubeUrl')
    if youtube_url:
        utils.youtube_download(youtube_url)
        
    else:
        print(f"[youtube-downloader] youtubeUrl not found in message")

def consume(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue='youtube-downloader')

    channel.basic_consume(queue='youtube-downloader', on_message_callback=callback, auto_ack=True)

    print('[youtube-downloader] Waiting for messages...')
    channel.start_consuming()
