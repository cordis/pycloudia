from zope.interface import Interface


class ISender(Interface):
    def send_package_by_decisive(decisive, activity, package):
        """
        :type decisive: C{str}
        :type activity: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """

    def send_package_by_identity(identity, activity, package):
        """
        :type identity: C{str}
        :type activity: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IRunner(Interface):
    def get_identity_by_decisive(decisive, activity):
        """
        :type decisive: C{str}
        :type activity: C{str}
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
    def get_item_by_hash(hash, groups=None):
        """
        :type decisive: C{str}
        :type groups: C{list} of C{str} or C{None}
        """


class IPackageProcessor(Interface):
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
