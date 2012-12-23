from datetime import datetime
from bson import ObjectId
from inspect import isclass

MONGO_TYPES = (ObjectId, int, float, basestring, list, dict, datetime)

def check_mongo_type(cls):
    """
    Returns `True` if cls could be stored in mongo,
    otherwise returns `False`
    """
    return issubclass(cls, MONGO_TYPES)


def type_name(obj_or_type):
    """
    Returns name of type.

    :param obj_or_type: It could be a type or an ordinary object.
        If obj is given, it returns the name of its type.
    """
    if isclass(obj_or_type):
        return obj_or_type.__name__
    return type(obj_or_type).__name__


def cast_to_class(value, cls):
    """
    Cast `value` to class.

    If `cls` has `cat_to_class` function, it would call it.
    Also support casting of primitive types: `unicode` to `str`,
    `str` to `unicode`, `int` to `float`. In other cases raises
    ValueError
    """
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
    """
    Return full python path of `obj`
    """
    return "%s.%s" % (obj.__module__, obj.__name__)


class ClassProperty(object):
    """
    Decorator for making property from `classmethod`

    Example of usage:
        class A(object):

         @ClassProperty
         def forty_two(cls):
            return 42

        print A.forty_two # Would print 42
    """

    def __init__(self, fget):
        """
        Construct `ClassProperty`, where fget is a get function
        """
        self.fget = fget

    def __get__(self, instance, owner):
        return self.fget(owner)