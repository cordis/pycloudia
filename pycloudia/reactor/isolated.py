from abc import ABCMeta, abstractmethod
from collections import deque

from pycloudia.uitls.defer import Deferred
from pycloudia.reactor.interfaces import IReactor, IIsolatedReactor
from pycloudia.reactor.reactive_queue import ReactiveQueueFactory


class IsolatedReactor(IIsolatedReactor):
    queue_factory = ReactiveQueueFactory()

    def __init__(self, reactor, count=100):
        """
        :type reactor: L{pycloudia.reactor.interfaces.IReactor}
        :type count: C{int}
        """
        self.reactor = reactor
        self.count = count
        self.state = InitialState(self)
        self.reactor.call_when_running(self.state.run)

    def isolate(self, hashable):
        return IsolatedReactorImplementation(self, hashable)

    def call_isolated(self, hashable, func, *args, **kwargs):
        return self.call_later_isolated(hashable, 0, func, *args, **kwargs)

    def call_later_isolated(self, hashable, seconds, func, *args, **kwargs):
        deferred = Deferred()
        task = self.queue_factory.create_task(func, args, kwargs, deferred)
        self.state.call_later(hashable, seconds, task)
        return deferred

    def create_queue(self):
        return self.queue_factory.create(self.reactor)

    def time(self):
        return self.reactor.time()

    def create_looping_call(self, func, *args, **kwargs):
        return self.reactor.create_looping_call(func, *args, **kwargs)

    def call_when_running(self, func, *args, **kwargs):
        self.reactor.call_when_running(func, *args, **kwargs)

    def register_for_shutdown(self, func, *args, **kwargs):
        self.reactor.register_for_shutdown(func, *args, **kwargs)

    def call_feature(self, name, *args, **kwargs):
        return self.reactor.call_feature(name, *args, **kwargs)

    def call(self, func, *args, **kwargs):
        return self.reactor.call(func, *args, **kwargs)

    def call_later(self, seconds, func, *args, **kwargs):
        return self.reactor.call_later(seconds, func, *args, **kwargs)


class IsolatedReactorImplementation(IReactor):
    def __init__(self, subject, hashable):
        """
        :type subject: L{pycloudia.reactor.interfaces.IIsolatedReactor}
        """
        self.subject = subject
        self.hashable = hashable

    def call(self, *args, **kwargs):
        self.subject.call(self.hashable, *args, **kwargs)

    def call_later(self, *args, **kwargs):
        self.subject.call_later(self.hashable, *args, **kwargs)


class BaseState(object):
    __metaclass__ = ABCMeta

    def __init__(self, subject):
        """
        :type subject: L{pycloudia.reactor.isolated.IsolatedReactor}
        """
        self.subject = subject

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    @abstractmethod
    def call_later(self, *args, **kwargs):
        raise NotImplementedError()


class InitialState(BaseState):
    def __init__(self, *args, **kwargs):
        super(InitialState, self).__init__(*args, **kwargs)
        self.task_list = deque()

    def call_later(self, *args, **kwargs):
        self.task_list.append((args, kwargs))

    def run(self):
        self.subject.state = state = RunningState(self.subject)
        for args, kwargs in self.task_list:
            state.call_later(*args, **kwargs)


class RunningState(BaseState):
    def __init__(self, *args, **kwargs):
        super(RunningState, self).__init__(*args, **kwargs)
        self.queue_list = [self.subject.create_queue() for x in range(self.subject.count)]

    def run(self):
        pass

    def call_later(self, seconds, task):
        func = self._get_queue(task.hashable).call
        self.subject.reactor.call_later(seconds, func, task)

    def _get_queue(self, hashable):
        return self.queue_list[hash(hashable) % self.subject.count]
