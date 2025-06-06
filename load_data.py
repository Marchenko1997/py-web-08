from mongoengine import connect
import json
from models import Quote, Author

connect(
    db="quotes_db",
    host="mongodb+srv://marchenkohalyna888:aAjz3jUlnkwNhUJY@cluster0.r5lerl8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
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
