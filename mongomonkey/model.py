from mongomonkey.utils import type_name

class ModelBase(type):

    def __new__(cls, name, bases, attributes):
        # Creating class
        module = attributes.pop('__module__')
        new_class = super(ModelBase, cls).__new__(cls, name, bases, {'__module__': module, '_meta': ModelMeta()})

        # Populating with attributes
        for name, attribute in attributes.viewitems():
            new_class.add_to_class(name, attribute)

        return new_class

    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class ModelMeta(object):
    """Class to store meta data about Model"""

    field_mapping = None
    attribute_field_mapping = None

    def __init__(self):
        self.field_mapping = {}
        # TODO: Add bidirectional mapping here
        self.attribute_field_mapping = {}

    def add_field(self, field, field_name, attribute_name):
        # Mapping 2 or more attribute to one field can cause lots of bugs.
        # So currently it is not allowed.
        if field_name in self.field_mapping:
            raise ValueError("Field %(field_name)s is already mapped." % {'field_name': field_name})
        self.field_mapping[field_name] = field
        self.attribute_field_mapping[attribute_name] = field_name


# TODO: We inherited our model from dict to simplify storing object in mongodb,
# but it allows to bypass fields validator to store data by accessing data through __setitem__.
# Is it critical and are there any other solutions?
class Model(dict):
    __metaclass__ = ModelBase

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if key in self._meta.field_mapping:
            value = self._meta.field_mapping[key].prepare(value)
        return super(Model, self).__setitem__(key, value)

    def __repr__(self):
        params = u" ".join((key + u"=" + repr(value) for key, value in self.viewitems()))
        return u"<%(class_name)s %(params)s>" % {"class_name": type_name(self), "params": params}

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError("update expected at most 1 arguments, got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def setdefault(self, key, value=None):
        if key not in self:
            self[key] = value
        return self[key]

    @classmethod
    def cast_to_class(cls, document):
        if not isinstance(document, dict):
            raise TypeError("Type of document should be subclass of dict.")
        obj = cls()
        obj.update(document)
        return obj
