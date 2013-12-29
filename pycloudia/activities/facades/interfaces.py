from zope.interface import Interface, Attribute


class IService(Interface):
    def process_outgoing_package(facade_id, client_id, package):
        """
        :type facade_id: C{str}
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IListener(Interface):
    def start():
        """
        :raises L{pycloudia.activities.facades.exceptions.ListenFailedError}:
        """


class IClient(Interface):
    client_id = Attribute('client_id', ':type: C{str}')

    def send_message(message):
        """
        :type message: C{str}
        """


class IClientDirector(Interface):
    def client_id_factory():
        """
        :rtype: C{str}
        """

    def connection_made(client):
        """
        :type client: C{IClient}
        """

    def connection_done(client):
        """
        :type client: C{IClient}
        """

    def connection_lost(client, reason):
        """
        :type client: C{IClient}
        :type reason: C{str}
        """

    def read_message(client, message):
        """
        :type client: C{IClient}
        :type str message:
        """

    def send_package(package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
