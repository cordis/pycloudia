from functools import wraps

from pycloudia.uitls.defer import inline_callbacks, return_value, maybe_deferred
from pycloudia.cloud.consts import HEADER, STATUS
from pycloudia.cloud.interfaces import IPackage


__all__ = [
    'ResolverMeta',
    'resolve_errors',
    'resolve_method',
]


class ResolverMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super(ResolverMeta, mcs).__new__(mcs, name, bases, namespace)
        cls.exception_map = {}
        for base in bases:
            if hasattr(base, 'exception_map'):
                cls.exception_map.update(base.exception_map)
        cls.exception_map.update(dict(
            (method.__exception_type__, method)
            for method in namespace.values()
            if hasattr(method, '__exception_type__')
        ))
        return cls

    def resolve(cls, exception, logger=None):
        try:
            method = cls.exception_map[type(exception)]
        except KeyError:
            if logger:
                logger.exception(exception)
            else:
                raise exception
        else:
            return method.__exception_verbose__, method(exception)


class ResolverMethodDecorator(object):
    def __init__(self, exception_type, verbose=None):
        self.exception_type = exception_type
        self.verbose = verbose or exception_type.__name__

    def __call__(self, method):
        method.__exception_type__ = self.exception_type
        method.__exception_verbose__ = self.verbose
        return method


class ResolverDecorator(object):
    def __init__(self, resolver, logging=True):
        self.resolver = resolver
        self.logging = logging

    def __call__(self, func):

        @wraps(func)
        @inline_callbacks
        def decorator(subject, package, *args, **kwargs):
            assert isinstance(package, IPackage)
            try:
                response = yield maybe_deferred(func(subject, package, *args, **kwargs))
            except Exception as e:
                if self.logging:
                    verbose, content = self.resolver.resolve(e, subject.logger)
                else:
                    verbose, content = self.resolver.resolve(e)
                response = package.create_response(content, {
                    HEADER.STATUS: STATUS.FAILURE,
                    HEADER.REASON: verbose,
                })
            return_value(response)

        return decorator


resolve_errors = ResolverDecorator
resolve_method = ResolverMethodDecorator
