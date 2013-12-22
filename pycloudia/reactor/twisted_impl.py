from zope.interface import implementer

from pycloudia.reactor.interfaces import ReactorInterface, LoopingCallInterface
from pycloudia.uitls.defer import Deferred


@implementer(ReactorInterface)
class ReactorAdapter(object):

    @classmethod
    def create_instance(cls):
        """
        :rtype: C{ReactorInterface}
        """
        from twisted.internet import reactor
        return cls(reactor)

    def __init__(self, subject):
        """
        :param subject: C{twisted.internet.reactor}
        """
        self.subject = subject

    def register_for_shutdown(self, func, *args, **kwargs):
        """
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """
        self.subject.addSystemEventTrigger('before', 'shutdown', func, *args, **kwargs)

    def call_when_running(self, func, *args, **kwargs):
        """
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """
        self.subject.callWhenRunning(func, *args, **kwargs)

    def call(self, func, *args, **kwargs):
        """
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: C{pycloudia.utils.defer.Deferred}
        """
        return self.call_later(0, func, *args, **kwargs)

    def call_later(self, seconds, func, *args, **kwargs):
        """
        :param seconds: C{int}
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: C{pycloudia.utils.defer.Deferred}
        """
        def cancel_deferred(_):
            delayed_call.cancel()
        deferred = Deferred(cancel_deferred)
        deferred.addCallback(lambda _: func(*args, **kwargs))
        delayed_call = self.subject.callLater(seconds, deferred.callback, None)
        return deferred

    def create_looping_call(self, func, *args, **kwargs):
        from twisted.internet.task import LoopingCall

        @implementer(LoopingCallInterface)
        class LoopingCallAdapter(LoopingCall):
            pass

        looping_call = LoopingCallAdapter(func, *args, **kwargs)
        looping_call.clock = self.subject
        return looping_call

    def call_feature(self, name, *args, **kwargs):
        """
        :type name: C{str}
        :param *args: Passed to feature
        :param **kwargs: Passed to feature
        :rtype: C{object} or C{None}
        """
        if not hasattr(self.subject, name):
            raise NotImplementedError(name)
        func = getattr(self.subject, name)
        if not callable(func):
            raise ValueError('Feature {0} is not callable'.format(name))
        return func(*args, **kwargs)
