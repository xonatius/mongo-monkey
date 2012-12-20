from datetime import datetime
from bson import ObjectId
from inspect import isclass

MONGO_TYPES = (ObjectId, int, float, basestring, list, dict, datetime)

def check_mongo_type(cls):
    return issubclass(cls, MONGO_TYPES)


def type_name(obj_or_type):
    """Returns name of type."""
    if isclass(obj_or_type):
        return obj_or_type.__name__
    return type(obj_or_type).__name__


def cast_to_class(value, cls):
    # Do not cast if type matched
    if isinstance(value, cls):
        return value
    # Calling cast_to_class if exists
    if hasattr(cls, 'cast_to_class'):
        return cls.cast_to_class(value)
    # Simple casting for primitive types
    if type(value) is int and cls is float:
        return float(value)
    if type(value) is str and cls is unicode:
        return unicode(value)
    if type(value) is unicode and cls is str:
        return str(value)
    # Other cases are not supported
    raise ValueError("Can't cast %(value)s to type %(cls_name)s" %
                     {'value':value, 'cls_name': type_name(cls)})


def get_path(obj):
    return "%s.%s" % (obj.__module__, obj.__name__)


class ClassProperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)