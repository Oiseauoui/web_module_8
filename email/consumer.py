import pika
import json
import threading
from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
print(' [*] Waiting for email messages. To exit press CTRL+C')


def process_email(ch, method, properties, body):
    message = json.loads(body.decode())
    contact_id = message["contact_id"]
    recipient_email = message["recipient_email"]

    # Retrieve contact from the database using the ObjectID
    contact = Contact.objects(id=contact_id).first()

    if contact:
        print(f" [x] Sending email to {recipient_email}")
        # Simulate a time-consuming email sending task
        # Set is_message_sent to True once sent
        contact.is_message_sent = True
        contact.save()
        print(f" [x] Email sent to {recipient_email}")
    else:
        print(f" [x] Contact not found for ID: {contact_id}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    # Create a new thread for processing the email message
    threading.Thread(target=process_email, args=(ch, method, properties, body)).start()


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()
