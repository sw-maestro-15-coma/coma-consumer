import pika, json, os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    host = os.environ.get('HOST')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue='video-download')
    data = {
        "videoId": "123",
        "youtubeUrl": "https://www.youtube.com/watch?v=123"
    }
    channel.basic_publish(exchange='', routing_key='video-download', body=json.dumps(data))
