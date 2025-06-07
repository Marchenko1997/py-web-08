import pika
from faker import Faker
from models import Contact
import json
import configparser
from mongoengine import connect
import random

config = configparser.ConfigParser()
config.read("config.ini")

db_name = config.get("DB", "DB_NAME")
db_user = config.get("DB", "DB_USER")
db_pass = config.get("DB", "DB_PASS")
db_domain = config.get("DB", "DB_DOMAIN")


connect(
    db=db_name,
    host=f"mongodb+srv://{db_user}:{db_pass}@{db_domain}/?retryWrites=true&w=majority&appName=Cluster0",
)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="contacts_email_queue", durable=True)
channel.queue_declare(queue="contacts_sms_queue", durable=True)

fake = Faker()

for _ in range(10):
    preferred_channel = random.choice(["email", "sms"])
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        preferred_channel=preferred_channel
    )
    contact.save()

    message = json.dumps({"id": str(contact.id)})

    queue_name = (
        "contacts_sms_queue" if preferred_channel == "sms" else "contacts_email_queue"
    )

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),
    )

    print(f"Sent contact id {contact.id} to queue.")

connection.close()
