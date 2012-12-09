MongoMonkey
============

MongoMonkey is a simple ODM for mongo.

Example of usage:
-------------

```python
from pymongo import Connection
from mongomonkey import Model, Field
from mongomonkey.data import list_of

class Book(Model):
    title = Field(unicode)
    page_count = Field(int)

    def __repr__(self):
        return u"<Book %(data)s>" % {'data': super(Book, self).__repr__()}

    @classmethod
    def create_book(cls, title=u"", page_count=0):
        book = cls()
        book.title = title
        book.page_count = page_count
        return book

class Author(Model):
    name = Field(unicode)
    books = Field(list_of(Book))

    def __repr__(self):
        return u"<Author %(data)s>" % {'data': super(Author, self).__repr__()}

connection = Connection()
db = connection.test_database
collection = db.test_collection

book1 = Book.create_book(u"Alice's Adventures in Wonderland", 191)
author = Author()
author.name = u"Lewis Carroll"
author.books = [book1, {u"title": u"A Tangled Tale", u"page_count": 152}]

# Saving object
collection.save(author)

# Retrieving object
author = collection.find_one(as_class=Author)
```
