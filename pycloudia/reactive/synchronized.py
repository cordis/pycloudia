from functools import wraps
from defer import defer as maybe_deferred

from pycloudia.reactive.queues import ReactiveQueueScope


__all__ = [
    'synchronized',
]


class Spec(object):
    """
    :type strategy: C{object}
    :type scope: C{object}
    :type args: C{int}
    :type key: C{str}
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
    args = None
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
    ATTRIBUTE = '__sync_queue__'

    queue_factory = ReactiveQueueScope

    @classmethod
    def create_instance(cls, instance, func, spec, io_loop):
        return cls(instance, func, spec, io_loop)

    def __init__(self, instance, func, spec, io_loop):
        """
        :type instance: C{object}
        :type func: C{Callable}
        :type spec: L{pycloudia.reactive.synchronized.Spec}
        """
        self.instance = instance
        self.func = func
        self.spec = spec
        self.io_loop = io_loop

    def __call__(self, *args, **kwargs):
        """
        :rtype: L{defer.Deferred}
        """
        queue = self._get_queue()
        key = self._create_queue_key(args)
        if not queue.is_empty(self.spec.key) or (self.spec.strategy is self.spec.STRATEGY.LOCK):
            return queue.call(self.spec.key, self.func, *args, **kwargs)
        return maybe_deferred(self.func, *args, **kwargs)

    def _get_queue(self):
        """
        :rtype: L{pycloudia.reactive.queues.ReactiveQueueScope}
        :raise: C{ValueError}
        """
        if self.spec.scope is self.spec.SCOPE.FUNC:
            return self._get_or_create_queue(self.func)
        elif self.spec.scope is self.spec.SCOPE.SELF:
            return self._get_or_create_queue(self.instance)
        else:
            raise ValueError('Unexpected spec scope: {0}'.format(self.spec.scope))

    def _get_or_create_queue(self, scope):
        """
        :type scope: C{object}
        :rtype: L{pycloudia.reactive.queues.ReactiveQueueScope}
        """
        if not hasattr(scope, self.ATTRIBUTE):
            setattr(scope, self.ATTRIBUTE, self.queue_factory(self.io_loop))
        return getattr(scope, self.ATTRIBUTE)

    def _create_queue_key(self, args):
        return '.'.join([self.spec.key] + map(str, args[:self.spec.args]))


class Factory(object):
    decorator_factory = Decorator.create_instance

    class Self(object):
        @staticmethod
        def lock(key=None, args=0):
            def decorator(func):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.LOCK
                spec.scope = spec.SCOPE.SELF
                spec.args = args
                spec.key = key
                return func
            return decorator

        @staticmethod
        def when(key=None, args=0):
            def decorator(func):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.WHEN
                spec.scope = spec.SCOPE.SELF
                spec.args = args
                spec.key = key
                return func
            return decorator

    class Func(object):
        @staticmethod
        def lock(key=None):
            def decorator(func, args=0):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.LOCK
                spec.scope = spec.SCOPE.FUNC
                spec.args = args
                spec.key = key
                return func
            return decorator

        @staticmethod
        def when(key=None):
            def decorator(func, args=0):
                spec = Spec.get_or_create_spec(func)
                spec.strategy = spec.STRATEGY.WHEN
                spec.scope = spec.SCOPE.FUNC
                spec.args = args
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
                decorator = cls.decorator_factory(instance, method, spec, io_loop)
                decorator = wraps(method)(decorator)
                setattr(instance, method_name, decorator)
        return instance

    @staticmethod
    def _get_io_loop():
        from tornado.ioloop import IOLoop
        return IOLoop.instance()


synchronized = Factory()
