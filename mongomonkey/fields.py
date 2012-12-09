from mongomonkey.utils import type_name, cast_to_class, check_mongo_type


# TODO: Implement default value. It's a tricky feature.
class Field(object):

    _cls = None
    _field_name = None

    _field_type = None

    # TODO: Make optional store type behavior: when field is not strongly typed,
    # we should keep type of EmbeddedModel in mongodb
    def __init__(self, field_type=None):
        if field_type is not None and not check_mongo_type(field_type):
            raise TypeError("Invalid mongo type %(type)s" % {'type': type_name(field_type)})

        self._field_type = field_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            if self._field_name in instance:
                return instance[self._field_name]
            raise AttributeError("'%(type_name)s' object has no attribute '%(field_name)s'" %
                                 {'type_name': type_name(owner), 'field_name': self._field_name})

    def __set__(self, instance, value):
        instance[self._field_name] = value

    def __delete__(self, instance):
        if instance is not None:
            if self._field_name in instance:
                del instance[self._field_name]

    def prepare(self, value):
        #TODO: Here could be implemented validation
        return self.ensure_type(value)

    def ensure_type(self, value):
        # If Field is not strongly typed, no preparation is need
        if self._field_type is None:
            return value
            # If value is None, no preparation is need
        if value is None:
            return value
            # If value is Dictionary and type is Model we should create model with data from dict
        return cast_to_class(value, self._field_type)

    def contribute_to_class(self, cls, name):
        # Attaching field to class
        setattr(cls, name, self)

        # Storing necessary data
        self._cls = cls
        self._field_name = name

        # Adding field to meta information of model
        self._cls._meta.add_field(self, self._field_name)

