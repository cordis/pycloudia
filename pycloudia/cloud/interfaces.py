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


class IActivity(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def service_name(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def decisive(self):
        """
        :rtype: C{Hashable}
        """

    @abstractproperty
    def identity(self):
        """
        :rtype: C{object}
        """


class ISender(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def package_factory(self, content, headers=None):
        """
        :type content: C{dict}
        :type headers: C{None} or C{dict}
        """

    @abstractmethod
    def send_request_package(self, source_activity, target_activity, package, timeout=0):
        """
        :type source_activity: L{pycloudia.cloud.interfaces.IActivity}
        :type target_activity: L{pycloudia.cloud.interfaces.IActivity}
        :type package: L{pycloudia.cloud.interfaces.IRequestPackage}
        :type timeout: C{int}
        """

    @abstractmethod
    def send_package(self, target_activity, package):
        """
        :type target_activity: L{pycloudia.cloud.interfaces.IActivity}
        :type package: L{pycloudia.cloud.interfaces.IRequestPackage}
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
        :rtype: L{pycloudia.cloud.interfaces.IServiceInvoker}
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
        :type package: L{pycloudia.cloud.interfaces.IRequestPackage}
        :rtype: L{Deferred} of L{pycloudia.cloud.interfaces.IRequestPackage}
        """


class IResponder(object):
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
