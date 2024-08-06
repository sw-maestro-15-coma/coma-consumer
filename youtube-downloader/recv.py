#!/usr/bin/env python
import pika, time, json

def callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    for key, value in data.items():
        print(f"{key}: {value}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")

def consume(host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages.')
    channel.start_consuming()
