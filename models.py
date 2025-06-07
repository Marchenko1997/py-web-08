from mongoengine import Document, ListField, StringField, ReferenceField, BooleanField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author) 
    quote = StringField()


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    preferred_channel = StringField(choices=["sms", "email"], required=True)
    is_sent = BooleanField(default=False)
