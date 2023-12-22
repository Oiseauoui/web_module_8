from mongoengine import connect
import json
from models import AuthorItem, QuoteItem

def load_authors(filename='authors.json'):
    with open(filename, 'r', encoding='utf-8') as authors_file:
        authors_data = json.load(authors_file)

    for author_data in authors_data:
        author = AuthorItem(**author_data)
        author.save()
        print(f"Author saved: {author.fullname}")

def load_quotes(filename='quotes.json'):
    with open(filename, 'r', encoding='utf-8') as quotes_file:
        quotes_data = json.load(quotes_file)

    for quote_data in quotes_data:
        author_fullname = quote_data['author']
        author = AuthorItem.objects(fullname=author_fullname).first()

        if author:
            quote_data['author'] = author
            quote = QuoteItem(**quote_data)
            quote.save()
            print(f"Quote saved: {quote.quote}")

        else:
            print(f"Author not found for quote: {quote_data}")

def search_quotes_by_author(author_name):
    author = AuthorItem.objects(fullname=author_name).first()
    if author:
        quotes = QuoteItem.objects(author=author)
        return quotes
    else:
        return []

def search_quotes_by_tag(tag):
    quotes = QuoteItem.objects(tags=tag)
    return quotes

def search_quotes_by_tags(tags):
    quotes = QuoteItem.objects(tags__in=tags)
    return quotes

if __name__ == '__main__':
    # Connect to MongoDB Atlas
    connect(db='home_08', host='mongodb+srv://oiseua:Kivusd4ST6eqoJDp@cluster0.no20xgq.mongodb.net/test?retryWrites=true&w=majority')

    # Load data into the database
    load_authors()
    load_quotes()

    while True:
        command = input("Enter command (e.g., name: Steve Martin, tag: life, tags: life, live, exit): ").strip()

        if command.lower() == 'exit':
            print("Exiting the program.")
            break

        parts = command.split(':')
        if len(parts) != 2:
            print("Invalid command format. Please try again.")
            continue

        key, value = parts
        key = key.strip().lower()
        value = value.strip()

        # Add a shortcut for searching by name and tag
        if key == 'name' and len(value) >= 2:
            if value[:2].lower() == 'st':
                value = 'Steve Martin'
        elif key == 'tag' and len(value) >= 2:
            if value[:2].lower() == 'li':
                value = 'life'

        if key == 'name':
            quotes = search_quotes_by_author(value)
        elif key == 'tag':
            quotes = search_quotes_by_tag(value)
        elif key == 'tags':
            tags = [tag.strip() for tag in value.split(',')]
            quotes = search_quotes_by_tags(tags)
        else:
            print("Unknown command. Please try again.")
            continue

        print("Search results:")
        for quote in quotes:
            print(f"{quote.author.fullname}: {quote.quote.encode('utf-8')}")
