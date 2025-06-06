from models import Author, Quote

while True:
    command = input("Enter a command: ")
    if command == "exit":
        break

    elif command.startswith('name:'):
        name = command.split(':', 1)[1].strip()
        author = Author.odjects(fullname=name).first()
        quotes = Quote.objects(author=author)

        for q in quotes:
            print(q.quote)

    elif command.startswith('tag:'):
        tag = command.split(':', 1)[1].strip()
        quotes = Quote.objects(tags=tag)
        for q in quotes:
            print(q.quote)
    
    elif command.startswith('tags:'):
        tags = command.split(':', 1)[1].split(',')
        quotes = Quote.objects(tags__in=tags)
        for q in quotes:
            print(q.quote)
