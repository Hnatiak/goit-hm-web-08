import json
import pika
from models import Contact
from mongoengine import connect

# Підключення до MongoDB
connect(host='mongodb+srv://PythonDB:cud4BUXMwUmTI9A9@cluster0.zv0mgxq.mongodb.net/')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='web16_queue', durable=True)


def process_message(ch, method, properties, body):
    message = json.loads(body.decode())
    contact_id = message['contact_id']

    contact = Contact.objects(id=contact_id).first()
    if contact:
        # Simulate sending email
        print(f"Sending email to {contact.email}...")
        # Assume email sending succeeds
        contact.email_sent = True
        contact.save()
        print(f"Email sent to {contact.email}")
    else:
        print(f"Contact with id {contact_id} not found.")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='web16_queue', on_message_callback=process_message)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
