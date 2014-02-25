from functools import wraps
from defer import defer as maybe_deferred

from pycloudia.reactive.queues import ReactiveQueueScope


__all__ = [
    'synchronized',
]


class Spec(object):
    """
    :type scope: C{object}
    :type key: C{Hashable}
    """

    ATTRIBUTE = '__sync__'

    class STRATEGY(object):
        LOCK = 'lock'
        WHEN = 'when'

    class SCOPE(object):
        SELF = object()
        FUNC = object()

    strategy = None
    scope = None
    key = None

    @classmethod
    def get_or_create_spec(cls, func):
        """
        :rtype: L{pycloudia.reactive.decorators.Spec}
        """
        if not hasattr(func, cls.ATTRIBUTE):
            setattr(func, cls.ATTRIBUTE, cls())
        return getattr(func, cls.ATTRIBUTE)


class Decorator(object):
    ATTRIBUTE = '__sync__'

    queue_factory = ReactiveQueueScope

    def __init__(self, func, spec, io_loop):
        """
        :type func: C{Callable}
        :type spec: L{pycloudia.reactive.synchronized.Spec}
        """
        self.func = func
        self.spec = spec
        self.io_loop = io_loop

    def __call__(self, obj, *args, **kwargs):
        queue = self._get_queue(obj)
        if queue.is_busy(self.spec.key) or (self.spec.strategy is self.spec.STRATEGY.LOCK):
            return queue.call(self.spec.key, self.func, obj, *args, **kwargs)
        return maybe_deferred(self.func, obj, *args, **kwargs)

    def _get_queue(self, obj):
        if self.spec.scope == self.spec.SCOPE.FUNC:
            return self._get_or_create_queue(self.func)
        elif self.spec.scope == self.spec.SCOPE.SELF:
            return self._get_or_create_queue(obj)
        else:
            raise ValueError('Unexpected spec scope: {0}'.format(self.spec.scope))

    def _get_or_create_queue(self, scope):
        """
        :rtype: L{pycloudia.reactive.decorators.Spec}
        """
        if not hasattr(scope, self.ATTRIBUTE):
            setattr(scope, self.ATTRIBUTE, self.queue_factory(self.io_loop))
        return getattr(scope, self.ATTRIBUTE)


class Factory(object):
    class Self(object):
        @staticmethod
        def lock(key=None):
            def decorator(func):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.LOCK
                spec.scope = spec.SCOPE.SELF
                spec.key = key
                return func
            return decorator

        @staticmethod
        def when(key=None):
            def decorator(func):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.WHEN
                spec.scope = spec.SCOPE.SELF
                spec.key = key
                return func
            return decorator

    class Func(object):
        @staticmethod
        def lock(key=None):
            def decorator(func):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.LOCK
                spec.scope = spec.SCOPE.FUNC
                spec.key = key
                return func
            return decorator

        @staticmethod
        def when(key=None):
            def decorator(func):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.WHEN
                spec.scope = spec.SCOPE.FUNC
                spec.key = key
                return func
            return decorator

    self = Self()
    func = Func()

    @classmethod
    def patch(cls, instance, io_loop=None):
        io_loop = io_loop or cls._get_io_loop()
        for method_name in dir(instance):
            method = getattr(instance, method_name)
            try:
                spec = getattr(method, Spec.ATTRIBUTE)
            except AttributeError:
                continue
            else:
                decorator = Decorator(method, spec, io_loop)
                decorator = wraps(method)(decorator)
                setattr(instance, method_name, decorator)
        return instance

    @staticmethod
    def _get_io_loop():
        from tornado.ioloop import IOLoop
        return IOLoop.instance()


synchronized = Factory()
