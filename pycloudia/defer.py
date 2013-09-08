from functools import wraps

from twisted.internet.defer import inlineCallbacks, maybeDeferred, returnValue, DeferredList

__all__ = [
    'inline_callbacks',
    'maybe_deferred',
    'return_value',
    'deferrable',
    'DeferredList'
]

inline_callbacks = inlineCallbacks
maybe_deferred = maybeDeferred
return_value = returnValue


def deferrable(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return maybe_deferred(function, *args, **kwargs)
    return wrapper
