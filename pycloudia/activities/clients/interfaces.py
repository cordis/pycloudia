from zope.interface import Interface


class IService(Interface):
    def create_activity(client_id, facade_id):
        """
        :type client_id: C{str}
        :type facade_id: C{str}
        """

    def delete_activity(client_id, reason=None):
        """
        :type client_id: C{str}
        :type reason: C{str}
        """

    def process_incoming_package(client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """

    def process_outgoing_package(client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
