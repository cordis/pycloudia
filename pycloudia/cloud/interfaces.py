from zope.interface import Interface


class ISender(Interface):
    def send_package_by_decisive(decisive, service, package):
        """
        :type decisive: C{str}
        :type service: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """

    def send_package_by_identity(identity, service, package):
        """
        :type identity: C{str}
        :type service: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IRunner(Interface):
    def get_identity_by_decisive(decisive, service):
        """
        :type decisive: C{str}
        :type service: C{str}
        """

    def send_message(identity, message):
        """
        :type identity: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IReader(Interface):
    def read_message(message):
        """
        :type message: C{str}
        """


class IMapper(Interface):
    def attach(item):
        """
        :type item: C{str}
        """

    def detach(item):
        """
        :type item: C{str}
        """

    def balance(hashable_list):
        """
        :type hashable_list: C{list} of C{Hashable}
        :rtype: C{list} of C{tuple} consisted of (C{Hashable} hashable, C{str} item_source, C{str} item_target)
        """

    def get_item_by_hashable(hashable):
        """
        :type hashable: C{Hashable}
        """


class IServiceAdapter(Interface):
    def create_activity(*args):
        pass

    def remove_activity(*args):
        pass

    def suspend_activity(*args):
        pass

    def recover_activity(*args):
        pass


class IServiceInvoker(Interface):
    def process_package(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class ISortedSet(Interface):
    def insert(item):
        """
        :type item: C{object}
        """

    def remove(item):
        """
        :type item: C{object}
        """


class ISequenceSpread(Interface):
    def spread(sequence, capacity):
        """
        :type sequence: C{collections.Sequence}
        :type capacity: C{int}
        :rtype: C{collections.Iterable}
        """
