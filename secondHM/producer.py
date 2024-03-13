import json
import pika
from datetime import datetime
from models import Contact
from mongoengine import connect

# Підключення до MongoDB
connect(host='mongodb+srv://PythonDB:cud4BUXMwUmTI9A9@cluster0.zv0mgxq.mongodb.net/')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange="web16_exchange", exchange_type="direct")
channel.queue_declare(queue='web16_queue', durable=True)
channel.queue_bind(exchange='web16_exchange', queue='web16_queue')


def create_contacts(num_contacts: int):
    for i in range(num_contacts):
        contact = Contact(
            full_name=f"John Doe {i}",
            email=f"john.doe{i}@example.com"
        )
        contact.save()

        message = {
            'contact_id': str(contact.id)
        }

        channel.basic_publish(exchange="web16_exchange", routing_key='web16_queue', body=json.dumps(message))

    connection.close()

if __name__ == '__main__':
    create_contacts(10)





















# import json
# import pika
# from datetime import datetime
# from models import Contact
#
# credentials = pika.PlainCredentials('guest', 'guest')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
# channel = connection.channel()
#
# channel.exchange_declare(exchange="web16_exchange", exchange_type="direct")
# channel.queue_declare(queue='web16_queue', durable=True)
# channel.queue_bind(exchange='web16_exchange', queue='web16_queue')
#
#
# def create_contacts(num_contacts: int):
#     for i in range(num_contacts):
#         contact = Contact(
#             full_name=f"John Doe {i}",
#             email=f"john.doe{i}@example.com"
#         )
#         contact.save()
#
#         message = {
#             'contact_id': str(contact.id)
#         }
#
#         channel.basic_publish(exchange="web16_exchange", routing_key='web16_queue', body=json.dumps(message))
#
#     connection.close()
#
# if __name__ == '__main__':
#     create_contacts(10)









# import json
# import pika
# from faker import Faker
#
# credentials = pika.PlainCredentials('guest', 'guest')
# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
# channel = connection.channel()
#
# channel.exchange_declare(exchange='web16_exchange', exchange_type='direct')
# channel.queue_declare(queue='web_16_queue', durable=True)
# channel.queue_bind(exchange='web16_exchange', queue='web_16_queue')
#
# def create_contacts(num_contacts):
#     fake = Faker()
#     for _ in range(num_contacts):
#         contact = {
#             'contact_id': fake.uuid4(),
#             'full_name': fake.name(),
#             'email': fake.email(),
#             'email_sent': False
#         }
#         yield contact
#
# def main():
#     contacts = create_contacts(10)
#
#     for contact in contacts:
#         channel.basic_publish(
#             exchange='web16_exchange',
#             routing_key='web_16_queue',
#             body=json.dumps(contact),
#             properties=pika.BasicProperties(delivery_mode=2)
#         )
#
#     print(" [x] Sent contacts to RabbitMQ")
#     connection.close()
#
# if __name__ == '__main__':
#     main()