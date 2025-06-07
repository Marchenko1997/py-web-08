from mongoengine import connect
import json
from models import Quote, Author
import configparser

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

with open("authors.json", "r") as f:
    authors = json.load(f)

for author in authors:
    a = Author(**author)
    a.save()

with open("qoutes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

for quote in quotes:
    author = Author.objects(fullname=quote["author"]).first()

    q = Quote(
        tags = quote["tags"],
        author = author,
        quote = quote["quote"],
    )

    q.save()
