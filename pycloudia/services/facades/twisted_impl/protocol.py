from twisted.protocols.basic import NetstringReceiver
from twisted.internet.protocol import Factory
from twisted.internet.protocol import connectionDone

from pycloudia.services.facades.interfaces import IClient


class Protocol(NetstringReceiver, IClient):
    factory = None
    client_id_factory = None

    def __init__(self):
        self.client_id = None

    def connectionMade(self):
        self.client_id = self.client_id_factory()
        self.factory.connection_made(self)

    def connectionLost(self, reason=connectionDone):
        if self.brokenPeer or reason is not connectionDone:
            self.factory.connection_lost(self, reason)
        else:
            self.factory.connection_done(self)

    def stringReceived(self, message):
        self.factory.read_message(self, message)

    def send_message(self, message):
        self.sendString(message)


class ProtocolServerFactory(Factory):
    protocol = Protocol

    def __init__(self, director):
        """
        :type director: L{pycloudia.activities.facades.interfaces.IClientDirector}
        """
        self.director = director

    def buildProtocol(self, address):
        protocol = Factory.buildProtocol(self, address)
        protocol.client_id_factory = self.director.client_id_factory
        return protocol

    def connection_made(self, protocol):
        self.director.connection_made(protocol)

    def connection_lost(self, protocol, reason):
        self.director.connection_lost(protocol, reason)

    def connection_done(self, protocol):
        self.director.connection_done(protocol)

    def read_message(self, protocol, message):
        self.director.read_message(protocol, message)
