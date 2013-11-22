from pycloudia.reactor.interfaces import ReactorInterface
from pycloudia.uitls.defer import inline_callbacks, Deferred, deferrable
from pycloudia.channels.txzmq_impl import SocketFactory
from pycloudia.devices.consts import DEVICE
from pycloudia.devices.discovery.udp import DiscoveryUdpProtocol
from pycloudia.uitls.net import Address


class Agent(object):
    heartbeat_interval = DEVICE.UDP.HEARTBEAT_INTERVAL
    reactor = ReactorInterface()
    router = None
    broadcast = None

    def __init__(self, identity, address):
        self.identity = identity
        self.address = address
        self.heartbeat = None
        self.peers = {}

    @inline_callbacks
    def start(self):
        yield self._start_router()
        yield self._start_multicast()
        yield self._start_heartbeat()

    @deferrable
    def _start_router(self):
        self.router.signal_message.connect(self._process_router_package)
        self.router.start()

    @deferrable
    def _start_multicast(self):
        self.broadcast.signal_message.connect(self._process_multicast_message)
        self.start()

    @deferrable
    def _start_heartbeat(self):
        self.heartbeat = self.reactor.create_looping_call(self._send_heartbeat)
        self.heartbeat.start(self.heartbeat_interval)

    def _send_heartbeat(self):
        self.broadcast.send('BEACON')

    def _process_router_package(self, package):
        pass

    def _process_multicast_message(self, message, host):
        pass

    def get_or_create_peer(self, identity, address):
        pass


class AgentFactory(object):
    udp_host = DEVICE.UDP.HOST
    udp_port = DEVICE.UDP.PORT

    reactor = ReactorInterface()
    broadcast_factory = DiscoveryUdpProtocol
    zmq_socket_factory = SocketFactory()

    def __call__(self, identity, host, port, interface=''):
        instance = Agent(identity, address)
        instance.reactor = self.reactor
        instance.router = self.zmq_socket_factory.create_router(address)
        instance.broadcast = self.broadcast_factory(self.udp_host, self.udp_port, self.interface)
        instance.broadcast.reactor = self.reactor
        return instance
