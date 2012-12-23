from mongomonkey.model_manager import model_manager
from mongomonkey.utils import type_name, cast_to_class, check_mongo_type


# TODO: Implement default value. It's a tricky feature.
class Field(object):
    """
    Class for setting field in model
    """

    _cls = None
    _field_name = None
    _attribute_name = None

    _field_type = None

    # TODO: Make optional store type behavior: when field is not strongly typed,
    # we should keep type of EmbeddedModel in mongodb
    def __init__(self, field_type=None, field_name=None):
        """
        Construct a new field

        :param field_type: type which field would store. If set to None it could
            store any type.

        :param field_name: name of field in mongo document. If set to None it
            would be the same as field name. Any two field in one model can't
            have the same `field_name`.
        """
        if field_type is not None and not isinstance(field_type, basestring) and \
           not check_mongo_type(field_type):
            raise TypeError("Invalid mongo type %(type)s" % {'type': type_name(field_type)})

        self._field_type = field_type
        self._field_name = field_name

    def __get__(self, instance, owner):
        """
        Getter of field
        """
        if instance is None:
            return self
        else:
            if self._field_name in instance:
                return instance[self._field_name]
            raise AttributeError("'%(type_name)s' object has no attribute '%(field_name)s'" %
                                 {'type_name': type_name(owner), 'field_name': self._field_name})

    def __set__(self, instance, value):
        """
        Setter of field
        """
        instance[self._field_name] = value

    def __delete__(self, instance):
        """
        Deletter of field (=
        """
        if instance is not None:
            if self._field_name in instance:
                del instance[self._field_name]
            else:
                raise AttributeError("'%(type_name)s' object has no attribute '%(field_name)s'" %
                                     {'type_name': type_name(instance), 'field_name': self._field_name})

    @property
    def field_type(self):
        """
        Returns field type. In case it is not resolved, resolve it.
        """
        # In case if field_type specified by string, we should resolve it
        if isinstance(self._field_type, basestring):
            if self._field_type == "self":
                self._field_type = self._cls
            else:
                self._field_type = model_manager.resolve(self._field_type)
        return self._field_type

    def prepare(self, value):
        """
        Prepare `value` with all field constraints and returns prepared object to store.
        """
        #TODO: Here could be implemented validation
        return self.ensure_type(value)

    def ensure_type(self, value):
        """
        Cast `value` to type which field could store.
        """
        # If Field is not strongly typed, no preparation is need
        if self.field_type is None:
            return value
            # If value is None, no preparation is need
        if value is None:
            return value
            # If value is Dictionary and type is Model we should create model with data from dict
        return cast_to_class(value, self.field_type)

    def contribute_to_class(self, cls, name):
        """
        Used to attach a field to model

        :param cls: model to which field is attached

        :param name: name of attribute to which this field is attached
        """
        # Attaching field to class
        setattr(cls, name, self)

        # Storing necessary data
        self._cls = cls
        self._attribute_name = name

        if self._field_name is None:
            self._field_name = name

        # Adding field to meta information of model
        self._cls._meta.add_field(self, self._field_name, self._attribute_name)

