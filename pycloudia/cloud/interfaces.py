from abc import ABCMeta, abstractmethod


class ISender(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def package_factory(self, content, headers=None):
        """
        :type content: C{dict}
        :type headers: C{None} or C{dict}
        """

    @abstractmethod
    def send_package_by_decisive(self, decisive, service, package):
        """
        :type decisive: C{str}
        :type service: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """

    @abstractmethod
    def send_package_by_identity(self, identity, service, package):
        """
        :type identity: C{str}
        :type service: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IRunner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_identity_by_decisive(self, decisive, service):
        """
        :type decisive: C{str}
        :type service: C{str}
        """

    @abstractmethod
    def send_message(self, identity, message):
        """
        :type identity: C{str}
        :type message: C{str}
        """


class IReader(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_message(self, message):
        """
        :type message: C{str}
        """


class IMapper(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def attach(self, item):
        """
        :type item: C{str}
        """

    @abstractmethod
    def detach(self, item):
        """
        :type item: C{str}
        """

    @abstractmethod
    def balance(self, hashable_list):
        """
        :type hashable_list: C{list} of C{Hashable}
        :return: List of (hashable, item_source, item_target)
        :rtype: C{list} of (C{Hashable}, C{str}, C{str})
        """

    @abstractmethod
    def get_item_by_hashable(self, hashable):
        """
        :type hashable: C{Hashable}
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
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :rtype: L{Deferred} of L{pycloudia.packages.interfaces.IPackage}
        """


class ISortedSet(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, item):
        """
        :type item: C{object}
        """

    @abstractmethod
    def remove(self, item):
        """
        :type item: C{object}
        """


class ISequenceSpread(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def spread(self, sequence, capacity):
        """
        :type sequence: C{collections.Sequence}
        :type capacity: C{int}
        :rtype: C{collections.Iterable}
        """
