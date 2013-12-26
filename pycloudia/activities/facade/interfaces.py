from zope.interface import Interface


class IClient(Interface):
    def connection_made():
        """
        Protocol callback
        """

    def connection_lost():
        """
        Protocol callback
        """

    def read_message(message):
        """
        Protocol callback
        """


class IProtocol(Interface):
    def lose_connection():
        pass

    def send_message(message):
        pass


class IProtocolFactory(Interface):
    def build_protocol(address):
        """
        Called when a connection has been established to address.

        If None is returned, the connection is assumed to have been refused,
        and the Port will close the connection.

        :type address: (host, port)
        :param address: The address of the newly-established connection

        :rtype: None if the connection was refused, otherwise an object
                 providing L{pycloudia.activities.facade.interface.IProtocol}.
        """

    def start():
        """
        Called every time this is connected to a Port or Connector.
        """

    def stop():
        """
        Called every time this is disconnected from a Port or Connector.
        """
