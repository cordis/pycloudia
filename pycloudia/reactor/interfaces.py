from abc import ABCMeta, abstractmethod


class IReactor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def time(self):
        """
        :rtype: C{int}
        """

    @abstractmethod
    def register_for_shutdown(self, func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """

    @abstractmethod
    def call_when_running(self, func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """

    @abstractmethod
    def call(self, func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: L{pycloudia.utils.defer.Deferred}
        """

    @abstractmethod
    def call_later(self, seconds, func, *args, **kwargs):
        """
        :type seconds: C{int}
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: L{pycloudia.utils.defer.Deferred}
        """

    @abstractmethod
    def create_looping_call(self, func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: C{ILoopingCall}
        """

    @abstractmethod
    def call_feature(self, name, *args, **kwargs):
        """
        :type name: C{str}
        :param *args: Passed to feature
        :param **kwargs: Passed to feature
        :rtype: C{object} or None
        """


class ILoopingCall(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, interval, now=True):
        """
        :type interval: int
        :type now: bool
        """

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def reset(self):
        pass


class IIsolatedReactor(IReactor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def isolate(self, hashable):
        """
        :type hashable: C{Hashable}
        :rtype: L{pycloudia.reactor.interfaces.IReactor}
        """

    @abstractmethod
    def call_isolated(self, hashable, func, *args, **kwargs):
        """
        :type hashable: C{Hashable}
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: L{pycloudia.utils.defer.Deferred}
        """

    @abstractmethod
    def call_later_isolated(self, hashable, seconds, func, *args, **kwargs):
        """
        :type hashable: C{Hashable}
        :type seconds: C{int}
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: L{pycloudia.utils.defer.Deferred}
        """
