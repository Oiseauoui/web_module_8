from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)  # Змінено цю лінію коду
    quote = StringField(required=True)
