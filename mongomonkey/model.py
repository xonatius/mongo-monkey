
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
    mongo_field_mapping = None

    def __init__(self):
        self.field_mapping = {}
        self.mongo_field_mapping = {}

    def add_field(self, field, model_name, mongo_name):
        self.field_mapping[model_name] = field
        self.mongo_field_mapping[mongo_name] = field

    def populate_model_from_document(self, model, document):
        for key, value in document.viewitems():
            if key in self.mongo_field_mapping:
                self.mongo_field_mapping[key].set_from_mongo(model, value)
            else:
                model[key] = value



# TODO: We inherited our model from dict to simplify storing object in mongodb,
# but it allows to bypass fields validator to store data by accessing data through __setitem__.
# Is it critical and are there any other solutions?
class Model(dict):
    __metaclass__ = ModelBase

    @classmethod
    def from_mongo(cls, document):
        obj = cls()
        cls._meta.populate_model_from_document(obj, document)
        return obj
