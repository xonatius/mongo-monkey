from mongomonkey.model_manager import model_manager
from mongomonkey.utils import type_name, cast_to_class, ClassProperty

class TypedList(list):
    """
    Base class for strongly typed `list`

    Behaves as ordinary list. Expect `_inner_type` field for ensuring the type.
    On any assign it tries to cast item to `inner_type`.
    """

    def __init__(self, seq=()):
        self.extend(seq)

    def append(self, p_object):
        return super(TypedList, self).append(self.cast_inner_item(p_object))

    def extend(self, iterable):
        checked_iterable = (self.cast_inner_item(value) for value in iterable)
        return super(TypedList, self).extend(checked_iterable)

    def insert(self, index, p_object):
        return super(TypedList, self).insert(index, self.cast_inner_item(p_object))

    def __add__(self, other):
        # TODO: Make it better
        new_obj = type(self)(self)
        new_obj.extend(other)
        return new_obj

    def __setslice__(self, i, j, sequence):
        return super(TypedList, self).__setslice__(i, j, (self.cast_inner_item(item) for item in sequence))

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            value = (self.cast_inner_item(item) for item in value)
        else:
            value = self.cast_inner_item(value)
        return super(TypedList, self).__setitem__(key, value)

    @ClassProperty
    def inner_type(cls):
        if isinstance(cls._inner_type, basestring):
            # TODO: think about handling "self" qualifier
            cls._inner_type = model_manager.resolve(cls._inner_type)
        # TODO: we can erase property on a first run
        return cls._inner_type

    @classmethod
    def validate(cls, value):
        """
        Check wether we can store `value` in this list or not.
        """
        return isinstance(value, cls.inner_type)

    @classmethod
    def cast_to_class(cls, value):
        if not isinstance(value, (list, )):
            raise TypeError("Value should be list, not %(type)s" % {'type': type_name(value)})
        item_generator = (cls.cast_inner_item(item) for item in value)
        return cls(item_generator)

    @classmethod
    def cast_inner_item(cls, item):
        """
        Cast `value` to `inner_type`
        """
        return cast_to_class(item, cls.inner_type)


class TypedListBase(type):
    """
    Metaclass for strongly typed lists.
    """

    def __new__(cls, inner_type):
        """
        Create a new strongly typed list class.

        :param inner_type: A type of objects that new list would store.
            If string passed the inner_type would be resolved on a first usage
            by `model_manager`.
        """
        if isinstance(inner_type, basestring):
            inner_type_name = inner_type.rsplit('.', 1)[-1]
        else:
            inner_type_name = inner_type.__name__
        name = inner_type_name + "List"
        bases = (TypedList,)
        dict = {'_inner_type': inner_type}
        return super(TypedListBase, cls).__new__(cls, name, bases, dict)


_list_cache = {}

def list_of(inner_type):
    """
    Return a new strongly typed list class. Returns from cache if it was already created,
    otherwise creates a new list and put it in cache.

    :param inner_type: A type of objects that new list would store.
        If string passed the inner_type would be resolved on a first usage
        by `model_manager`.
    """
    # TODO: Better handling of qualifier?
    if inner_type not in _list_cache:
        _list_cache[inner_type] = TypedListBase(inner_type)
    return _list_cache[inner_type]