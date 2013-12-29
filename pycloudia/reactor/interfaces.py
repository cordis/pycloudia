from zope.interface import Interface


class IReactor(Interface):
    def time():
        """
        :rtype: C{int}
        """

    def register_for_shutdown(func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """

    def call_when_running(func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """

    def call(func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: L{pycloudia.utils.defer.Deferred}
        """

    def call_later(seconds, func, *args, **kwargs):
        """
        :type seconds: C{int}
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: L{pycloudia.utils.defer.Deferred}
        """

    def create_looping_call(func, *args, **kwargs):
        """
        :type func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: C{LoopingCallInterface}
        """

    def call_feature(name, *args, **kwargs):
        """
        :type name: C{str}
        :param *args: Passed to feature
        :param **kwargs: Passed to feature
        :rtype: C{object} or None
        """


class LoopingCallInterface(Interface):
    def start(interval, now=True):
        """
        :type interval: int
        :type now: bool
        """

    def stop():
        pass

    def reset():
        pass
