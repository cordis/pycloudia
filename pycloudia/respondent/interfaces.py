from abc import ABCMeta, abstractmethod


class IRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def listen(self, request_id, deferred, timeout):
        """
        :type request_id: C{str}
        :type deferred: L{Deferred}
        :type timeout: C{int}
        """

    @abstractmethod
    def resolve(self, request_id, *args, **kwargs):
        """
        :type request_id: C{str}
        """

    @abstractmethod
    def reject(self, request_id, reason):
        """
        :type request_id: C{str}
        :type reason: C{Exception}
        """


class IDao(object):
    __metaclass__ = ABCMeta
