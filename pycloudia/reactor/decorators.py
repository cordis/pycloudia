from functools import wraps, partial


def call_isolated(func_or_attr):
    def decorator_factory(attr, func):
        @wraps(func)
        def decorator(obj, hashable, *args, **kwargs):
            reactor = getattr(obj, attr)
            return reactor.call_isolated(hashable, func, obj, hashable, *args, **kwargs)
        return decorator

    if callable(func_or_attr):
        return decorator_factory('reactor', func_or_attr)
    else:
        return partial(decorator_factory, func_or_attr)
