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
        return super(TypedList, self).__setitem__(key, self.ensure_type(value))

    def __setslice__(self, i, j, sequence):
        check_iterable = (self.ensure_type(item) for item in sequence)
        return super(TypedList, self).__setslice__(i, j, check_iterable)

    @classmethod
    def ensure_type(cls, value):
        if not cls.validate(value):
            raise TypeError("Type of value should be %(expected)s, not %(actual)s" % {'expected': cls._inner_type, 'actual': type(value)})
        return value

    @classmethod
    def validate(cls, value):
        return isinstance(value, cls._inner_type)

    @classmethod
    def from_mongo(cls, value):
        if not isinstance(value, (list, )):
            raise TypeError("Value should be list, not %(type)s" % {'type': type(value)})
        item_generator = (cls.item_from_mongo(item) for item in value)
        return cls(item_generator)

    @classmethod
    def item_from_mongo(cls, item):
        if not isinstance(item, cls._inner_type):
            return cls._inner_type.from_mongo(item)
        return item


class TypedListBase(type):

    def __new__(cls, inner_type):
        name = inner_type.__name__ + 'List'
        bases = (TypedList,)
        dict = {'_inner_type': inner_type}
        return super(TypedListBase, cls).__new__(cls, name, bases, dict)

_list_cache = {}

def make_list(cls):
    if cls not in _list_cache:
        _list_cache[cls] = TypedListBase(cls)
    return _list_cache[cls]