from mongoengine import Document, StringField, BooleanField, connect

# Connect to the MongoDB database
connect('Db_email', host='mongodb+srv://oiseua:Kivusd4ST6eqoJDp@cluster0.no20xgq.mongodb.net/test?retryWrites=true&w=majority')


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True, unique=True)
    is_message_sent = BooleanField(default=False)
    # Add other fields as needed for additional information

    def __str__(self):
        return f"{self.full_name} ({self.email})"
