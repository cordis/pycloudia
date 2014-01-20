from abc import ABCMeta, abstractmethod, abstractproperty

from pycloudia.packages.interfaces import IPackage


class IRequestPackage(IPackage):
    __metaclass__ = ABCMeta

    @abstractproperty
    def content(self):
        """
        :rtype: C{dict} or C{str}
        """

    @abstractproperty
    def headers(self):
        """
        :rtype: C{dict}
        """

    @abstractmethod
    def create_response(self, content, headers):
        """
        :rtype: L{pycloudia.packages.interfaces.IPackage} or C{None}
        """


class ISender(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def package_factory(self, content, headers=None):
        """
        :type content: C{dict}
        :type headers: C{None} or C{dict}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """

    @abstractmethod
    def send_request_package(self, source, target, package, timeout=0):
        """
        :type source: L{pycloudia.cluster.beans.Activity}
        :type target: L{pycloudia.cluster.beans.Activity}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :type timeout: C{int}
        :rtype: L{Deferred}
        """

    @abstractmethod
    def send_package(self, target, package):
        """
        :type target: L{pycloudia.cluster.beans.Activity}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IReader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_message(self, message):
        """
        :type message: C{str}
        """


class IRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_identity_by_decisive(self, decisive):
        """
        :type decisive: C{Hashable}
        :rtype: C{object}
        """

    @abstractmethod
    def send_message(self, identity, message):
        """
        :type identity: C{str}
        :type message: C{str}
        """

    @abstractmethod
    def is_outgoing(self, identity):
        """
        :type identity: C{str}
        :rtype: C{bool}
        """

    @abstractmethod
    def get_service_invoker_by_name(self, name):
        """
        :type name: C{str}
        :rtype: L{pycloudia.cluster.interfaces.IServiceInvoker}
        """


class IMapper(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def attach(self, item):
        """
        :type item: C{Hashable}
        """

    @abstractmethod
    def detach(self, item):
        """
        :type item: C{Hashable}
        """

    @abstractmethod
    def balance(self, hashable_list):
        """
        :type hashable_list: C{list} of C{Hashable}
        :return: List of (hashable, item_source, item_target)
        :rtype: C{list} of (C{Hashable}, C{object}, C{object})
        """

    @abstractmethod
    def get_item_by_hashable(self, hashable):
        """
        :type hashable: C{Hashable}
        :rtype: C{object}
        """


class IServiceAdapter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def suspend_activity(self, *args):
        pass

    @abstractmethod
    def recover_activity(self, *args):
        pass


class IServiceInvoker(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_package(self, package):
        """
        :type package: L{pycloudia.cluster.interfaces.IRequestPackage}
        :rtype: L{Deferred} of L{pycloudia.cluster.interfaces.IRequestPackage}
        """
