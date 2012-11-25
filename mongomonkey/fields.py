from bson.objectid import ObjectId

from mongomonkey import Model
from mongomonkey.data import TypedList
from mongomonkey.utils import type_name

MONGO_TYPES = (ObjectId, int, float, basestring, list, dict)

def default_value_from_type(cls):
    if cls is not None and not issubclass(cls, Model):
        return cls()
    return None

def check_mongo_type(cls):
    return issubclass(cls, MONGO_TYPES)

class Field(object):

    _cls = None
    _field_name = None
    _attr_name = None
    _default_value = None

    _field_type = None

    # TODO: Make optional store type behavior: when field is not strongly typed, we should keep type of EmbeddedModel in mongodb
    def __init__(self, field_type=None, field_name=None, default_value=default_value_from_type):
        if field_type is not None and not check_mongo_type(field_type):
            raise TypeError("Invalid mongo type %(type)s" % {'type': field_type})

        self._field_name = field_name
        self._field_type = field_type
        self._default_value = default_value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            if self._field_name in instance:
                return instance[self._field_name]
            raise AttributeError("'%(type_name)s' object has no attribute '%(attr_name)s'" % {'type_name': type_name(owner), 'attr_name': self._attr_name})

    def __set__(self, instance, value):
        value = self.prepare(value)

        instance[self._field_name] = value

    def __delete__(self, instance):
        if instance is not None:
            if self._field_name in instance:
                del instance[self._field_name]

    def prepare(self, value):
        # If Field is not strongly typed, no preparation is need
        if self._field_type is None:
            return value
        # If value is None, no preparation is need
        if value is None:
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

    def set_default(self, instance):
        if callable(self._default_value):
            value = self._default_value(self._field_type)
        else:
            value = self._default_value
        self.__set__(instance, value)

    def contribute_to_class(self, cls, name):
        # Attaching field to class
        setattr(cls, name, self)

        # Storing necessary data
        self._cls = cls
        self._attr_name = name

        # Setting mapped_name to name of field if it wasn't set before
        if self._field_name is None:
            self._field_name = name

        # Adding field to meta information of model
        self._cls._meta.add_field(self, name, self._attr_name)

