from collections import deque

from pycloudia.utils.defer import inline_callbacks


class ReactiveQueueTask(object):
    def __init__(self, func, args, kwargs, deferred):
        """
        :type func: C{Callable}
        :type args: C{tuple}
        :type kwargs: C{dict}
        :type deferred: L{Deferred}
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.deferred = deferred

    def __call__(self):
        return self.func(*self.args, **self.kwargs)

    def resolve(self, ret):
        self.deferred.callback(ret)

    def reject(self, error):
        self.deferred.errback(error)


class ReactiveQueue(object):
    def __init__(self, reactor):
        """
        :type reactor: L{pycloudia.reactor.interfaces.IReactor}
        """
        self.reactor = reactor
        self.task_list = deque()
        self._is_busy = False

    def call(self, task):
        """
        :type task: L{pycloudia.reactor.lockable.ReactiveQueueTask}
        """
        self.task_list.append(task)
        self.tick()

    @inline_callbacks
    def tick(self):
        if not self._is_busy:
            self._is_busy = True
            task = self.task_list.popleft()
            try:
                ret = yield task()
                self.reactor.call(task.resolve, ret)
            except Exception as e:
                self.reactor.call(task.reject, e)
            finally:
                self._is_busy = False
                if self.task_list:
                    self.reactor.call(self.tick)


class ReactiveQueueFactory(object):
    @staticmethod
    def create_task(func, args, kwargs, deferred):
        return ReactiveQueueTask(func, args, kwargs, deferred)

    @staticmethod
    def create(reactor):
        return ReactiveQueue(reactor)
