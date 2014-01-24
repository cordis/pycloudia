from abc import ABCMeta, abstractmethod


class ICollection(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __iter__(self):
        """
        :rtype: C{Iterable}
        """


class IInvoker(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def initialize(self):
        """
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def run(self):
        """
        :rtype: L{Deferred} of C{None}
        """

    @abstractmethod
    def process_package(self, package):
        """
        :type package: L{pycloudia.cluster.interfaces.IRequestPackage}
        :rtype: L{Deferred} of L{pycloudia.cluster.interfaces.IRequestPackage}
        """


class IServiceChannelsFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_by_address(self, address):
        """
        :type address: C{str}
        :rtype: L{pycloudia.services.beans.Channel}
        """

    @abstractmethod
    def create_by_runtime(self, runtime):
        """
        :type runtime: C{str}
        :rtype: L{pycloudia.services.beans.Channel}
        """


class IChannelsFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_by_address(self, service, address):
        """
        :type service: C{str}
        :type address: C{str}
        :rtype: L{pycloudia.services.beans.Channel}
        """

    @abstractmethod
    def create_by_runtime(self, service, runtime):
        """
        :type service: C{str}
        :type runtime: C{str}
        :rtype: L{pycloudia.services.beans.Channel}
        """
