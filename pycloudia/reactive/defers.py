from functools import wraps
from defer import Deferred, inline_callbacks, return_value, defer as maybe_deferred


__all__ = [
    'inline_callbacks',
    'maybe_deferred',
    'return_value',
    'deferrable',
    'Deferred',
    'synchronized',
]


def deferrable(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        return maybe_deferred(func, *args, **kwargs)
    return decorator
