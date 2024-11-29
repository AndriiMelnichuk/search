import pika
import json

from .utils import filter_groups, get_groups, get_tasks4group, filter_tasks

def process_message(ch, method, properties, body):
    # Здесь будет обработка входящего запроса входящего вместо фласк
    message = json.loads(body)
    response = {}
    if message['type'] == 'task':
        jwt = message.get('jwt')
        group_id = message.get('group_id')
        text = message.get('text')
        assigned_to = message.get('assigned_to')
        complete_before = message.get('complete_before')
        todo = message.get('status')
        is_date = message.get('is_date')
        task_list = get_tasks4group(group_id, jwt)
        filtered_task_list = filter_tasks(task_list, text, assigned_to, complete_before, todo, is_date)  
        response = {
            'id': [t.id for t in filtered_task_list],
            'title': [t.name for t in filtered_task_list],
            'description': [t.description for t in filtered_task_list],
            'deadline': [t.deadline for t in filtered_task_list],
            'assigned': [t.assigned for t in filtered_task_list],
            'status': [t.todo for t in filtered_task_list],
        }
    else:
        jwt = message.get('jwt')
        text = message.get('text')
        group_list = get_groups(jwt)
        filtered_group_list = filter_groups(group_list, text)
        response = {
            "id": [group.id for group in filtered_group_list],
            "group": [group.name for group in filtered_group_list],
        }

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
