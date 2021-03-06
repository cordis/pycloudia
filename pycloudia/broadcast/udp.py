from pysigslot import Signal


class UdpMulticast(object):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IReactor}
    """
    reactor = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.adapter = self._create_protocol_adapter()
        self.on_read = Signal()

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
                self.transport.joinGroup(self.multicast.localhost)

            def send(self, message):
                self.transport.write(message, (self.multicast.localhost, self.multicast.port))

            def datagramReceived(self, data, address_tuple):
                self.multicast.on_read.emit(data, address_tuple[0])

        return ProtocolAdapter.create_instance(self)

    def start(self):
        self.reactor.call_feature(
            'listenMulticast',
            self.port,
            self.adapter,
            self.host,
            listenMultiple=True
        )

    def send_message(self, message):
        self.adapter.send(message)


class UdpMulticastFactory(object):
    factory = UdpMulticast

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __call__(self):
        return self.factory(self.host, self.port)
