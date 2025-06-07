from mongoengine import connect, Q
from models import Author, Quote
import redis
from redis_lru import RedisLRU
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


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_by_name(name):

    author = Author.objects(Q(fullname__iregex=f"^{name}")).first()
    if author:
        quotes = Quote.objects(author=author)
        return [q.quote for q in quotes]
    else:
        return []


@cache
def search_by_tag(tag):
    quotes = Quote.objects(tags__iregex=f"^{tag}")
    return [q.quote for q in quotes]


while True:
    command = input("Enter a command: ")
    if command == "exit":
        break

    elif command.startswith("name:"):
        name = command.split(":", 1)[1].strip()
        result = search_by_name(name)
        for q in result:
            print(q)

    elif command.startswith("tag:"):
        tag = command.split(":", 1)[1].strip()
        result = search_by_tag(tag)
        for q in result:
            print(q)

    elif command.startswith("tags:"):
        tags = command.split(":", 1)[1].split(",")
        quotes = Quote.objects(tags__in=tags)
        for q in quotes:
            print(q.quote)
