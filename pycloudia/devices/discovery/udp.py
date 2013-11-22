from twisted.internet.protocol import DatagramProtocol

from pycloudia.reactor.interfaces import ReactorInterface
from pycloudia.uitls.defer import inline_callbacks
from pycloudia.uitls.net import Address


class DiscoveryUdpProtocol(DatagramProtocol):
    reactor = ReactorInterface()
    address_factory = Address

    def __init__(self, host, port, interface=''):
        self.address = self.address_factory(host, port)
        self.interface = interface
        self.signal_message = Signal()

    def start(self):
        self.reactor.call_feature(
            'listenMulticast',
            self.address.port,
            self,
            self.interface,
            listenMultiple=True
        )

    @inline_callbacks
    def startProtocol(self):
        yield self.transport.joinGroup(self.host)

    def send(self, message):
        self.transport.write(message, self.address)

    def datagramReceived(self, data, address_tuple):
        self.signal_message.emit(data, self.address_factory(*address_tuple))
