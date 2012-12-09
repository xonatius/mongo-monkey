from mongomonkey.utils import type_name

class TypedList(list):

    def __init__(self, seq=()):
        self.extend(seq)

    def append(self, p_object):
        return super(TypedList, self).append(self.ensure_type(p_object))

    def extend(self, iterable):
        checked_iterable = (self.ensure_type(value) for value in iterable)
        return super(TypedList, self).extend(checked_iterable)

    def insert(self, index, p_object):
        return super(TypedList, self).insert(index, self.ensure_type(p_object))

    def __add__(self, other):
        # TODO: Make it better
        new_obj = type(self)(self)
        new_obj.extend(other)
        return new_obj

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            value = (self.ensure_type(item) for item in value)
        else:
            value = self.ensure_type(value)
        return super(TypedList, self).__setitem__(key, value)

    @classmethod
    def ensure_type(cls, value):
        if not cls.validate(value):
            raise TypeError("Type of value should be %(expected)s, not %(actual)s" %
                            {'expected': type_name(cls._inner_type), 'actual': type_name(value)})
        return value

    @classmethod
    def validate(cls, value):
        return isinstance(value, cls._inner_type)

    @classmethod
    def cast_to_class(cls, value):
        if not isinstance(value, (list, )):
            raise TypeError("Value should be list, not %(type)s" % {'type': type_name(value)})
        item_generator = (cls.cast_inner_item(item) for item in value)
        return cls(item_generator)

    @classmethod
    def cast_inner_item(cls, item):
        if not isinstance(item, cls._inner_type):
            #TODO: Check cast_to_class existance
            return cls._inner_type.cast_to_class(item)
        return item


class TypedListBase(type):

    def __new__(cls, inner_type):
        name = inner_type.__name__ + 'List'
        bases = (TypedList,)
        dict = {'_inner_type': inner_type}
        return super(TypedListBase, cls).__new__(cls, name, bases, dict)

_list_cache = {}

def list_of(cls):
    if cls not in _list_cache:
        _list_cache[cls] = TypedListBase(cls)
    return _list_cache[cls]