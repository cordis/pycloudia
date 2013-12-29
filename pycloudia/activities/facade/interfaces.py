from zope.interface import Interface


class IListener(Interface):
    def start():
        """
        :raises C{pycloudia.activities.facade.exceptions.ListenFailedError}:
        """


class IClient(Interface):
    def connection_made():
        """
        Protocol callback
        """

    def connection_done():
        """
        Protocol callback
        """

    def connection_lost(reason):
        """
        Protocol callback
        :param str reason:
        """

    def read_message(message):
        """
        Protocol callback
        :param str message:
        """


class IClientDirector(Interface):
    def create_client(protocol):
        """
        :rtype: C{pycloudia.activities.facade.interfaces.IClient}
        """
