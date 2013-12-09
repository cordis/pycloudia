from functools import partial

from pycloudia.reactor.interfaces import ReactorInterface
from pycloudia.devices.consts import DEVICE
from pycloudia.devices.discovery.udp import UdpMulticastProtocol
from pycloudia.zmq_impl.factory import SocketFactory


class Peer(object):
    def __init__(self, identity):
        self.identity = identity

    def connect(self, host, port):
        pass


class Beacon(object):
    @classmethod
    def create_from_str(cls, beacon_str):
        port, identity = beacon_str.split(':')
        return cls(port, identity)

    def __init__(self, port, identity):
        self.port = port
        self.identity = identity

    def __str__(self):
        return ':'.join([self.port, self.identity])


class Agent(object):
    heartbeat_interval = DEVICE.UDP.HEARTBEAT_INTERVAL
    reactor = ReactorInterface
    zmq_socket_factory = SocketFactory()
    beacon_factory = Beacon
    broadcast = None

    def __init__(self, host, identity):
        self.host = host
        self.identity = identity
        self.router = None
        self.heartbeat = None
        self.dealers = {}

    def start(self):
        port = self._start_router()
        self._start_broadcast(port)

    def _start_router(self):
        self.router = self.zmq_socket_factory.create_router_socket()
        self.router.message_received.connect(self._process_router_message)
        return self.router.start_on_random_port(self.host)

    def _start_broadcast(self, port):
        beacon_str = str(self.beacon_factory(port, self.identity))
        self.broadcast.message_received.connect(self._process_broadcast_message)
        self.broadcast.start()
        self.heartbeat = self.reactor.create_looping_call(partial(self.broadcast.send, beacon_str))
        self.heartbeat.start(self.heartbeat_interval)

    def _process_broadcast_message(self, message, host):
        beacon = self.beacon_factory.create_from_str(message)
        peer = self.get_or_create_dealer(host, beacon.port, beacon.identity)
        peer.prolongate()

    def get_or_create_dealer(self, host, port, identity):
        dealer = self.dealers[identity] = self.zmq_socket_factory.create_dealer_socket(identity)
        dealer.sndhwm = DEVICE.UDP.PEER_EXPIRED * 100
        dealer.sndtimeo = 0
        dealer.message_received.connect(self._process_dealer_message)
        dealer.start(host, port)
        return dealer

    def _process_router_message(self, message):
        pass

    def _process_dealer_message(self, message):
        pass


class AgentFactory(object):
    udp_host = DEVICE.UDP.HOST
    udp_port = DEVICE.UDP.PORT

    reactor = ReactorInterface
    broadcast_factory = UdpMulticastProtocol
    zmq_socket_factory = SocketFactory()

    def __init__(self, zmq_socket_factory):
        self.zmq_socket_factory = zmq_socket_factory

    def __call__(self, identity, host, interface=''):
        instance = Agent(host, identity)
        instance.reactor = self.reactor
        instance.zmq_socket_factory = self.zmq_socket_factory
        instance.broadcast = self._create_broadcast(interface)
        return instance

    def _create_broadcast(self, interface):
        instance = self.broadcast_factory(self.udp_host, self.udp_port, interface)
        instance.reactor = self.reactor
        return instance
