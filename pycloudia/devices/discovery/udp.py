from twisted.internet.protocol import DatagramProtocol

from pycloudia.uitls.defer import inline_callbacks, maybe_deferred
from pycloudia.uitls.net import Address
from pycloudia.devices.consts import DEVICE


class DiscoveryUdpProtocol(DatagramProtocol):
    address = Address(DEVICE.UDP.HOST, DEVICE.UDP.PORT)

    def __init__(self, callback):
        self.callback = callback
        self.start_callback = lambda _: None

    def set_start_callback(self, func):
        self.start_callback = lambda _: func()

    @inline_callbacks
    def startProtocol(self):
        yield self.transport.joinGroup(self.address.host)
        yield maybe_deferred(self.start_callback)

    def send(self, message):
        self.transport.write(message, self.address)

    def datagramReceived(self, data, address):
        self.callback(data, Address(*address))
