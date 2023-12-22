from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField


class AuthorItem(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class QuoteItem(Document):
    tags = ListField(StringField())
    author = ReferenceField(AuthorItem)  # Змінено цю лінію коду
    quote = StringField(required=True)

