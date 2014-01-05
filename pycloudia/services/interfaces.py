from abc import ABCMeta, abstractmethod


class IActivity(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self):
        """
        :rtype: L{Deferred}
        """

    @abstractmethod
    def start(self):
        """
        :rtype: L{Deferred}
        """


class IActivityFactory(object):
    __metaclass__ = ABCMeta
