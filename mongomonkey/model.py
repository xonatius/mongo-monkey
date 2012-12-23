from mongomonkey.model_manager import model_manager
from mongomonkey.utils import type_name

class ModelBase(type):
    """
    Metaclass for all models
    """

    def __new__(cls, name, bases, attributes):
        """
        Constructing a new model class
        """
        # Creating class
        module = attributes.pop('__module__')
        new_class = super(ModelBase, cls).__new__(cls, name, bases, {'__module__': module, '_meta': ModelMeta()})

        # Populating with attributes
        for name, attribute in attributes.viewitems():
            new_class.add_to_class(name, attribute)

        # Registering model in model manager
        model_manager.register_model(new_class)

        return new_class

    def add_to_class(cls, name, value):
        """
        Attaching attributes to class
        """
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class ModelMeta(object):
    """
    Class to store meta data about `Model`
    """

    field_mapping = None
    attribute_field_mapping = None

    def __init__(self):
        """
        Constructing `ModelMeta`
        """
        self.field_mapping = {}
        # TODO: Add bidirectional mapping here
        self.attribute_field_mapping = {}

    def add_field(self, field, field_name, attribute_name):
        """
        Adding field to metadata

        :param field: field which attached to model

        :param field_name: name of field in mongo document

        :param attribute_name: name of attribute in model
        """
        # Mapping 2 or more attribute to one field can cause lots of bugs.
        # So currently it is not allowed.
        if field_name in self.field_mapping:
            raise ValueError("Field %(field_name)s is already mapped." % {'field_name': field_name})
        self.field_mapping[field_name] = field
        self.attribute_field_mapping[attribute_name] = field_name


# TODO: We inherited our model from dict to simplify storing object in mongodb,
# but it allows to bypass fields validator to store data by accessing data through __setitem__.
# Is it critical and are there any other solutions?
class Model(dict):
    """
    Base class for declaring all models

    Has interface as ordinary dict, but handle process specially if item
    is mapped to fields.

    Example of usage:

        class Book(Model):
            title = Field(unicode)
            date = Field(datetime)
            page_count = Field(int)

        class Author(Model):
            id = Field(ObjectId, u'_id')
            name = Field(unicode)
            books = Field(list_of("Book"))

        book1 = Book(title=u"Alice's Adventures in Wonderland", page_count=191, date=datetime(1865, 11, 26))
        author = Author(name=u"Lewis Carroll")
        # Accessing by field
        author.books = [book1]
        # Accessing like dict
        author['books'].append({{u"title": u"A Tangled Tale", u"page_count": 152}})
        author['some_other_field'] = 42

    To work with models you can simply use `pymongo` syntax. For example,
    to store model in mongodb you can use `save` (also, by default pymongo will add
    `_id` field to document):

        connection = Connection()
        db = connection.test_database
        collection = db.test_collection
        collection.save(author)
        print author['_id']

    To retrieve document from mongodb and map it to model you can use `find`
    or `find_one` with `as_class` parameter:

        author = collection.find_one(as_class=Author)
    """

    __metaclass__ = ModelBase

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in self._meta.field_mapping:
            value = self._meta.field_mapping[key].prepare(value)
        return super(Model, self).__setitem__(key, value)

    def __repr__(self):
        params = u" ".join((key + u"=" + repr(value) for key, value in self.viewitems()))
        return u"<%(class_name)s %(params)s>" % {"class_name": type_name(self), "params": params}

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("update expected at most 1 arguments, got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]

    @classmethod
    def cast_to_class(cls, document):
        """
        Cast given `document` to this Model
        """
        if not isinstance(document, dict):
            raise TypeError("Type of document should be subclass of dict.")
        obj = cls()
        obj.update(document)
        return obj
