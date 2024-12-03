import pika
import json
from .utils import on_task, on_group

def process_message(ch, method, properties, body):
    # Здесь будет обработка входящего запроса входящего вместо фласк
    message = json.loads(body)
    response = {}
    if message['type'] == 'task':
        response = on_task(message)
    elif message['type'] == 'group':
        response = on_group(message)


    print(f"[x] Received message: {message}")
    if properties.reply_to:
        response_queue = properties.reply_to
        correlation_id = properties.correlation_id
        # Відправка відповіді на чергу
        ch.basic_publish(
            exchange='',
            routing_key=response_queue,
            properties=pika.BasicProperties(
                reply_to=properties.reply_to,
                correlation_id=correlation_id
            ),
            body=json.dumps(response)
        )
        print(f"[*] Sent response: {response}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer(queue_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            'rabbitmq', 
            5672,   # RabbitMQ port
            '/',    # Virtual host
            pika.PlainCredentials('admin', 'password')
        )
    )
    channel = connection.channel()
    
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=process_message)
    print(f"[*] Waiting for messages in {queue_name}")
    channel.start_consuming()
