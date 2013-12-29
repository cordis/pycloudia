from twisted.protocols.basic import NetstringReceiver
from twisted.internet.protocol import Factory
from twisted.internet.protocol import connectionDone


class Protocol(NetstringReceiver):
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

    def __init__(self, subject):
        self.subject = subject

    def buildProtocol(self, address):
        protocol = Factory.buildProtocol(self, address)
        protocol.client_id_factory = self.subject.client_id_factory
        return protocol

    def connection_made(self, protocol):
        self.subject.connection_made(protocol.client_id, protocol.send_message)

    def connection_lost(self, protocol, reason):
        self.subject.connection_lost(protocol.client_id, reason)

    def connection_done(self, protocol):
        self.subject.connection_done(protocol.client_id)

    def read_message(self, protocol, message):
        self.subject.read_message(protocol.client_id, message)
