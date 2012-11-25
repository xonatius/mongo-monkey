
def type_name(obj_or_type):
    """Returns name of type."""
    if issubclass(obj_or_type, type):
        return obj_or_type.__name__
    return type(obj_or_type).__name__
