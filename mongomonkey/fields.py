from mongomonkey.data import TypedList

MONGO_TYPES = (int, float, basestring, list, dict)

def check_mongo_type(cls):
    return issubclass(cls, MONGO_TYPES)

class Field(object):

    _cls = None
    _field_name = None
    _mapped_name = None

    _field_type = None

    # TODO: Make optional store type behavior: when field is not strongly typed, we should keep type of EmbeddedModel in mongodb
    def __init__(self, field_type=None, field_name=None):
        if field_type is not None and not check_mongo_type(field_type):
            raise TypeError("Invalid mongo type %(type)s" % {'type': field_type})

        self._field_name = field_name
        self._field_type = field_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.get(self._field_name, None)

    def __set__(self, instance, value):
        value = self.prepare(value)

        instance[self._field_name] = value

    def __delete__(self, instance):
        if instance is not None:
            if self._field_name in instance:
                del instance[self._field_name]

    def prepare(self, value):
        # If Field is not strongly typed, no preparation is need
        # TODO: Here we should implement store type behavior
        if self._field_type is None:
            return value
        # If value type doesn't match, we should raise an exception
        if not isinstance(value, self._field_type):
            raise TypeError("Type of value should be %(expected)s, not %(actual)s" % {'expected': self._field_type, 'actual': type(value)})
        # Special handling for list if expected list is strongly typed
        if issubclass(self._field_type, TypedList):
            return self._field_type(value)
        # Everything else returns without modification
        return value

    def set_from_mongo(self, instance, mongo_value):
        if hasattr(self._field_type, 'from_mongo'):
            instance[self._field_name] = self._field_type.from_mongo(mongo_value)
        else:
            instance[self._field_name] = mongo_value

    def contribute_to_class(self, cls, name):
        # Attaching field to class
        setattr(cls, name, self)

        # Storing necessary data
        self._cls = cls
        self._field_name = name

        # Setting mapped_name to name of field if it wasn't set before
        if self._mapped_name is None:
            self._mapped_name = name

        # Adding field to meta information of model
        self._cls._meta.add_field(self, name, self._mapped_name)

