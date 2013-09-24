from functools import wraps

from twisted.internet.defer import inlineCallbacks, maybeDeferred, returnValue, DeferredList, Deferred

__all__ = [
    'inline_callbacks',
    'maybe_deferred',
    'return_value',
    'deferrable',
    'DeferredListFactory',
    'Deferred',
]

inline_callbacks = inlineCallbacks
maybe_deferred = maybeDeferred
return_value = returnValue


def deferrable(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return maybe_deferred(function, *args, **kwargs)
    return wrapper


class DeferredListFactory(DeferredList):
    @staticmethod
    def create_all_or_nothing(deferred_list):
        def restore_failure(failure):
            return failure.value.subFailure
        instance = DeferredList(deferred_list, fireOnOneErrback=True, consumeErrors=True)
        instance.addErrback(restore_failure)
        return instance
