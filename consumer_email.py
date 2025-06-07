import pika
import json
import time
from models import Contact
import configparser
from mongoengine import connect

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


def send_email(contact):
    print(f"Sending EMAIL to {contact.email} ...")
    time.sleep(1)
    print(f"EMAIL sent to {contact.email}")


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="contacts_email_queue", durable=True)


def callback(ch, method, properties, body):
    message = json.loads(body.decode())

    contact_id = message["id"]
    contact = Contact.objects(id=contact_id).first()

    if contact and not contact.is_sent:
        send_email(contact)
        contact.is_sent = True
        contact.save()
        print(f"Contact {contact.email} updated to is_sent=True")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
print("Waiting for EMAIL messages. To exit press CTRL+C")
channel.basic_consume(queue="contacts_email_queue", on_message_callback=callback)
channel.start_consuming()
