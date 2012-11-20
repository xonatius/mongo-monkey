
# TODO: Add IntField, StringField etc.
class Field(object):

    _cls = None
    _field_name = None
    _mapped_name = None

    def __init__(self):
        pass

    def __get__(self, instance, owner):
        if instance is None:
            # TODO: Think here about implementing quering in mongo.
            # Car(Model):
            #    number = Field()
            #
            #
            # Car.number == 1 should generate {'number': 1}
            return self
        else:
            return instance.__mongodocument__.get(self._field_name, None)

    def __set__(self, instance, value):
        instance.__mongodocument__[self._field_name] = value

    def contribute_to_class(self, cls, name):
        # Attaching field to class
        setattr(cls, name, self)

        # Storing necessary data
        self._cls = cls
        self._field_name = name

        # Setting mapped_name to name of field if it wasn't set before
        if self._mapped_name is None:
            self._mapped_name = name


class ModelBase(type):

    def __new__(cls, name, bases, attributes):
        # Creating class
        module = attributes.pop('__module__')
        new_class = super(ModelBase, cls).__new__(cls, name, bases, {'__module__': module})

        # Populating with attributes
        for name, attribute in attributes.items():
            new_class.add_to_class(name, attribute)

        return new_class

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class Model(object):
    __metaclass__ = ModelBase

    def __init__(self, mongo_document = None):
        # Create a dictionary to store data from mongo
        # TODO: Think about another solutions
        if mongo_document is None:
            mongo_document = {}
        else:
            if not isinstance(mongo_document, dict):
                raise TypeError("Type of mongo_document should be subclass of dict")
            # Copying mongo_document as dict
            mongo_document = dict(mongo_document)
        self.__mongodocument__ = mongo_document or {}

    def to_document(self):
        # TODO: Protecting from writing?
        return self.__mongodocument__

    # TODO: Make automapping with cursor and collection
