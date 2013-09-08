from functools import wraps
from types import GeneratorType


def collect_list(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        ret = function(*args, **kwargs)
        if isinstance(ret, GeneratorType):
            ret = list(ret)
        return ret

    return decorator


def generate_dict(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        ret = function(*args, **kwargs)
        if not isinstance(ret, GeneratorType):
            return ret
        data = {}
        for item in ret:
            if isinstance(item, dict):
                data.update(item)
            else:
                key, value = item
                data[key] = value
        return data

    return decorator
