#!/usr/bin/env python
import pika, json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='54.180.140.202'))
channel = connection.channel()

channel.queue_declare(queue='hello')

body = {
   "videoId": 1,
   "shortsId": 1,
   "youtubeUrl": "hello",
}
json_body = json.dumps(body)

channel.basic_publish(exchange='', routing_key='hello', body=json_body)
print(f" [x] Sent {json_body}")
connection.close()