from collection import deque

from pycloudia.uitls.defer import Deferred, inline_callbacks
from pycloudia.reactor.interfaces import ReactorInterface


class ReactorCollection(object):
    def __init__(self, reactor, count=50):
        assert ReactorInterface.implementedBy(reactor)
        self.reactor = reactor
        self.count = count
        self.state = InitialState(self)

    def run(self):
        self.state.run()

    def get(self, hashable):
        return HashableReactor(self, hashable)

    def call_entirely(self, hashable, func, *args, **kwargs):
        return self.call_entirely_later(hashable, 0, func, *args, **kwargs)

    def call_entirely_later(self, hashable, seconds, func, *args, **kwargs):
        if callable(seconds):
            seconds, func = hashable, seconds
            args = list(args)
            args.insert(0, func)
            hashable = None
        deferred = Deferred()
        self.state.call_later(hashable, seconds, ReactiveQueueTask(func, args, kwargs, deferred))
        return deferred


class HashableReactor(object):
    def __init__(self, subject, hashable):
        self.subject = subject
        self.hashable = hashable

    def call(self, *args, **kwargs):
        self.subject.call(self.hashable, *args, **kwargs)

    def call_later(self, *args, **kwargs):
        self.subject.call_later(self.hashable, *args, **kwargs)


class BaseState(object):
    def __init__(self, subject):
        self.subject = subject

    def run(self):
        raise NotImplementedError()

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
        self.queue_list = [ReactiveQueue(self.subject.reactor) for x in range(self.subject.count)]

    def run(self):
        pass

    def call_later(self, seconds, task):
        func = self._get_queue(task.hashable).call
        self.subject.reactor.call_later(seconds, func, task)

    def _get_queue(self, hashable):
        return self.queue_list[hash(hashable) % self.subject.count]


class ReactiveQueueTask(object):
    def __init__(self, func, args, kwargs, deferred):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.deferred = deferred

    def __call__(self):
        return self.func(*self.args, **self.kwargs)

    def resolve(self, ret):
        self.deferred.callback(ret)


class ReactiveQueue(object):
    def __init__(self, reactor):
        self.reactor = reactor
        self.task_list = deque()
        self._is_busy = False

    def call(self, task):
        self.task_list.append(task)
        self._run_next_task()

    @inline_callbacks
    def _run_next_task(self):
        if not self._is_busy:
            self._is_busy = True
            task = self.task_list.popleft()
            try:
                ret = yield task()
                self.reactor.call(task.resolve, ret)
            finally:
                self._is_busy = False
                if self.task_list:
                    self.reactor.call(self._run_next_task)
