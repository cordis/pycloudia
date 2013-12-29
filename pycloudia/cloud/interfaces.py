from zope.interface import Interface


class IBroker(Interface):
    def send_package_by_decisive(decisive, activity, package):
        """
        :type decisive: C{str}
        :type activity: C{str}
        :type package: C{pycloudia.packages.interfaces.IPackage}
        """

    def send_package_by_identity(identity, activity, package):
        """
        :type identity: C{str}
        :type activity: C{str}
        :type package: C{pycloudia.packages.interfaces.IPackage}
        """


class IPackageProcessor(Interface):
    def process_package(package):
        """
        :type package: C{pycloudia.packages.interfaces.IPackage}
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
