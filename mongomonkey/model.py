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

    def __init__(self):
        self.field_mapping = {}

    def add_field(self, field, name):
        self.field_mapping[name] = field


# TODO: We inherited our model from dict to simplify storing object in mongodb,
# but it allows to bypass fields validator to store data by accessing data through __setitem__.
# Is it critical and are there any other solutions?
class Model(dict):
    __metaclass__ = ModelBase

    def __setitem__(self, key, value):
        if key in self._meta.field_mapping:
            value = self._meta.field_mapping[key].prepare(value)
        return super(Model, self).__setitem__(key, value)

    #TODO: Update, __init__ and other populating stuff

    @classmethod
    def cast_to_class(cls, document):
        if not isinstance(document, dict):
            raise TypeError() #TODO: Msg
        obj = cls()
        for key, value in document.viewitems():
            obj[key] = value
        return obj
