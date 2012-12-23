from mongomonkey.utils import get_path

class ModelManager(object):
    """
    ModelManager store all constructed model classes
    """

    models = None
    name_to_path = None

    def __init__(self):
        self.models = {}
        self.name_to_path = {}

    def register_model(self, model):
        """
        Register new model class
        """
        self.models[get_path(model)] = model
        if model.__name__ not in self.name_to_path:
            self.name_to_path[model.__name__] = []
        self.name_to_path[model.__name__].append(get_path(model))

    def resolve(self, path_or_name):
        """
        Returns model class by its name or full python path.
        """
        if '.' not in path_or_name:
            name = path_or_name
            if name in self.name_to_path:
                paths = self.name_to_path[name]
                if len(paths) == 1:
                    path = paths[0]
                else:
                    # TODO: Change ValueError to sth else
                    raise ValueError("Ambiguous name \"%(name)s\". Variants are: %(variants)s"
                                     % {'name': name, 'variants': ",".join(paths)})
            else:
                raise ValueError("Can't resolve model by name \"%(name)s\" " % {'name': name})
        else:
            path = path_or_name
        if path not in self.models:
            raise ValueError("Can't resolve model by path \"%(path)s\" " % {'path': path})
        return self.models[path]


model_manager = ModelManager()

