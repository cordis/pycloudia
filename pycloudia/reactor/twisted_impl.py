from zope.interface import implements

from pycloudia.reactor.interfaces import ReactorInterface


class ReactorAdapter(object):
    implements(ReactorInterface)

    @classmethod
    def create_instance(cls):
        from twisted.internet import reactor
        return cls(reactor)

    def __init__(self, subject):
        self.subject = subject

    def register_for_shutdown(self, func):
        self.subject.addSystemEventTrigger('before', 'shutdown', func)

    def call_when_running(self, func):
        self.subject.callWhenRunning(func)

    def run(self):
        self.subject.run()

    def call(self, func, *args, **kwargs):
        self.call_later(0, func, *args, **kwargs)

    def call_later(self, seconds, func, *args, **kwargs):
        self.subject.callLater(seconds, func, *args, **kwargs)
