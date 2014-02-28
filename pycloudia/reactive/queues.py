from collections import deque
from defer import inline_callbacks, Deferred


class ReactiveQueue(object):
    def __init__(self, io_loop):
        """
        :type io_loop: L{tornado.ioloop.IOLoop}
        """
        self.io_loop = io_loop
        self.task_list = deque()
        self._is_busy = False

    def is_empty(self):
        return not self.is_busy() and not bool(self.task_list)

    def is_busy(self):
        return self._is_busy

    def call(self, task):
        self.task_list.append(task)
        self.tick()

    @inline_callbacks
    def tick(self):
        if not self._is_busy:
            self._is_busy = True
            task = self.task_list.popleft()
            try:
                ret = yield task()
                self.io_loop.add_callback(task.resolve, ret)
            except Exception as e:
                self.io_loop.add_callback(task.reject, e)
            finally:
                self._is_busy = False
                if self.task_list:
                    self.io_loop.add_callback(self.tick)


class ReactiveQueueTask(object):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.deferred = Deferred()

    def __call__(self):
        return self.func(*self.args, **self.kwargs)

    def resolve(self, ret):
        self.deferred.callback(ret)

    def reject(self, error):
        self.deferred.errback(error)


class ReactiveQueueScope(object):
    queue_factory = ReactiveQueue
    task_factory = ReactiveQueueTask

    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.queue_map = {}

    def is_empty(self, key):
        try:
            return self.queue_map[key].is_empty()
        except KeyError:
            return True

    def is_busy(self, key):
        try:
            return self.queue_map[key].is_busy()
        except KeyError:
            return False

    def call(self, key, func, *args, **kwargs):
        task = self.task_factory(func, args, kwargs)
        queue = self._get_or_create_queue(key)
        queue.call(task)
        return task.deferred

    def _get_or_create_queue(self, key):
        try:
            queue = self.queue_map[key]
        except KeyError:
            queue = self.queue_map[key] = self.queue_factory(self.io_loop)
        return queue
