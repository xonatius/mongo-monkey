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

class Author(Model):
    name = Field(unicode)
    books = Field(list_of(Book))

connection = Connection()
db = connection.test_database
collection = db.test_collection

book1 = Book(title=u"Alice's Adventures in Wonderland", page_count=191)
author = Author(name=u"Lewis Carroll")
author.books = [book1, {u"title": u"A Tangled Tale", u"page_count": 152}]

# Saving object
collection.save(author)

# Retrieving object
author = collection.find_one(as_class=Author)
```
