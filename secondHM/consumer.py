import json
import pika

def send_email_stub(contact_id):
    print(f"Email sent to contact with ID: {contact_id}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received message: {message}")

    send_email_stub(message['contact_id'])

    # Для того щоб змінити на True
    # contact = Contact.objects.get(id=message['contact_id'])
    # contact.email_sent = True
    # contact.save()

    print(f"Email sent to contact with ID: {message['contact_id']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(queue='web_16_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='web_16_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    main()