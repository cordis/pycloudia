from abc import ABCMeta, abstractproperty, abstractmethod


class IAgentConfig(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def host(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def min_port(self):
        """
        :rtype: C{int}
        """

    @abstractproperty
    def max_port(self):
        """
        :rtype: C{int}
        """

    @abstractproperty
    def identity(self):
        """
        :rtype: C{str}
        """


class IRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        pass
