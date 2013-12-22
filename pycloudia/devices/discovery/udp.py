from pysigslot import Signal

from pycloudia.reactor.interfaces import ReactorInterface


class UdpMulticast(object):
    reactor = ReactorInterface

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.adapter = self._create_protocol_adapter()
        self.message_received = Signal()

    def _create_protocol_adapter(self):
        from twisted.internet.protocol import DatagramProtocol

        class ProtocolAdapter(DatagramProtocol):
            multicast = None

            @classmethod
            def create_instance(cls, multicast):
                instance = cls()
                instance.multicast = multicast
                return instance

            def startProtocol(self):
                self.transport.joinGroup(self.multicast.host)

            def send(self, message):
                self.transport.write(message, (self.multicast.host, self.multicast.port))

            def datagramReceived(self, data, address_tuple):
                self.multicast.message_received.emit(data, address_tuple[0])

        return ProtocolAdapter.create_instance(self)

    def start(self):
        self.reactor.call_feature(
            'listenMulticast',
            self.port,
            self.adapter,
            self.host,
            listenMultiple=True
        )

    def send(self, message):
        self.adapter.send(message)
