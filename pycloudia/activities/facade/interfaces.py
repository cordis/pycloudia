from zope.interface import Interface, Attribute


class IListener(Interface):
    def start():
        """
        :raises C{pycloudia.activities.facade.exceptions.ListenFailedError}:
        """


class IClient(Interface):
    client_id = Attribute(''':type client_id: str''')

    def send_message(message):
        """
        :param C{str} message:
        """


class IClientDirector(Interface):
    def client_id_factory():
        """
        :rtype: C{str}
        """

    def connection_made(client):
        """
        :param C{IClient} client:
        """

    def connection_done(client):
        """
        :param C{IClient} client:
        """

    def connection_lost(client, reason):
        """
        :param C{IClient} client:
        :param C{str} reason:
        """

    def read_message(client, message):
        """
        :param C{IClient} client:
        :param str message:
        """

    def send_package(package):
        """
        :param C{pycloudia.packages.interfaces.IPackage} package:
        """
