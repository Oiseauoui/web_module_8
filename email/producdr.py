import pika
import json
from datetime import datetime
from faker import Faker  # Install with: pip install Faker
from models import Contact

fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='email_exchange', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='email_exchange', queue='email_queue')


def generate_fake_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contact(full_name=full_name, email=email)
        contact.save()
        contacts.append(contact)
    return contacts


def main():
    num_contacts = 15
    contacts = generate_fake_contacts(num_contacts)

    for contact in contacts:
        message = {
            "contact_id": str(contact.id),
            "recipient_email": contact.email,
            "subject": "Your Subject",
            "body": "Your Email Body",
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange='email_exchange',
            routing_key='email_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f" [x] Sent email to {contact}")
    connection.close()


if __name__ == '__main__':
    main()
