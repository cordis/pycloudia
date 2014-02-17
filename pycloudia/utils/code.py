from importlib import import_module


class ImproperlyConfiguredError(RuntimeError):
    pass


def instantiate_by_config(default_cls, config, factory=None):
    if config is None:
        cls = default_cls()
        options = {}
    elif isinstance(config, str):
        cls = import_class(config)
        options = {}
    elif isinstance(config, dict):
        options = config.get('options', {})
        if 'path' not in config:
            cls = default_cls
        elif isinstance(config['path'], str):
            cls = import_class(config['path'])
        else:
            raise ImproperlyConfiguredError('Unable to find an alternative to %s' % default_cls)
    else:
        raise ImproperlyConfiguredError('Unable to find an alternative to %s' % default_cls)

    if not factory:
        return cls(**options)

    return factory(cls, **options)


def import_class(path):
    module_name, cls_name = path.split(':')
    module = import_module(module_name)
    name_chunks = cls_name.split('.')
    obj = getattr(module, name_chunks[0])
    for chunk in name_chunks[1:]:
        obj = getattr(obj, chunk)
    return obj
