MongoMonkey
============

MongoMonkey is a simple ODM for mongo.
The key idea was to use standard pymongo api, without overriding it.

Example of usage:
-------------

```python
from pymongo import Connection
from mongomonkey import Model, Field, list_of

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
# Accessing by field attribute
author.books = [book1]
# Accessing like dict item
author['books'].append({u"title": u"A Tangled Tale", u"page_count": 152})

# Saving object
collection.save(author) # By default pymongo would attach '_id' to this document.

# Retrieving object
author = collection.find_one(as_class=Author)
```

Recursive embedding:
-------------

```python
from mongomonkey import Model, Field, list_of

class Node(Model):
    title = Field(unicode)
    # You can use 'self' to point on currently creating Model
    child1 = Field('self')
    # Also you can use a name of a model to point on it
    child2 = Field('Node')

# Printing instance of Node
print Node(title=u"root", child1=Node(title=u"Child1"), child2=Node(title=u"Child2"))
```

Developing and Contributing
-------------

If you have any question, ideas or improvements feel free to fork or add an issue
on github http://github.com/xonatius/mongo-monkey