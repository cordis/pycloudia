from zope.interface import Interface


class ReactorInterface(Interface):
    def register_for_shutdown(func, *args, **kwargs):
        """
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """

    def call_when_running(func, *args, **kwargs):
        """
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        """

    def run():
        pass

    def call(func, *args, **kwargs):
        """
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: C{pycloudia.utils.defer.Deferred}
        """

    def call_later(seconds, func, *args, **kwargs):
        """
        :param seconds: C{int}
        :param func: C{callable}
        :param *args: Passed to C{func}
        :param **kwargs: Passed to C{func}
        :rtype: C{pycloudia.utils.defer.Deferred}
        """
