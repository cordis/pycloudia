from importlib import import_module


def import_class(path):
    module_name, cls_name = path.split(':')
    module = import_module(module_name)
    name_chunks = cls_name.split('.')
    obj = getattr(module, name_chunks[0])
    for chunk in name_chunks[1:]:
        obj = getattr(obj, chunk)
    return obj
