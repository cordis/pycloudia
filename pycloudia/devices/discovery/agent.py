from functools import partial

from pysigslot import Signal

from pycloudia.reactor.interfaces import ReactorInterface


class Peer(object):
    heartbeat = None

    def __init__(self, identity, dealer):
        self.identity = identity
        self.dealer = dealer


class Agent(object):
    reactor = ReactorInterface
    protocol = None
    broadcast = None
    zmq_socket_factory = None
    peer_factory = None

    def __init__(self, identity, config):
        self.identity = identity
        self.config = config

        self.dealer_created = Signal()
        self.dealer_deleted = Signal()

        self.router = None
        self.heartbeat = None
        self.udp_beacon_message = None
        self.zmq_beacon_message = None

        self.peer_map = {}

    def start(self):
        port = self._start_router()
        self._create_beacons(port)
        self._start_broadcast()
        self._start_heartbeat()

    def _start_router(self):
        self.router = self.zmq_socket_factory.create_router_socket()
        self.router.message_received.connect(self._process_router_message)
        return self.router.start_on_random_port(self.config.host, self.config.min_port, self.config.max_port)

    def _create_beacons(self, port):
        self.udp_beacon_message = self.protocol.create_udp_beacon_message(self.config.host, port, self.identity)
        self.zmq_beacon_message = self.protocol.create_zmq_beacon_message(self.config.host, port, self.identity)

    def _start_broadcast(self):
        self.broadcast.message_received.connect(self._process_broadcast_message)
        self.broadcast.start()

    def _start_heartbeat(self):
        self.heartbeat = self.reactor.create_looping_call(self.broadcast.send, self.udp_beacon_message)
        self.heartbeat.start(self.protocol.udp_heartbeat_interval)

    def _process_router_message(self, message):
        try:
            peer = self.peer_map[message.peer]
            self._reset_peer_heartbeat(peer)
        except KeyError:
            assert self.protocol.is_beacon(message)
            beacon = self.protocol.parse_zmq_beacon_message(message, message.peer)
            self._process_beacon(beacon)

    def _process_broadcast_message(self, message, host):
        if self.protocol.is_beacon(message):
            beacon = self.protocol.parse_udp_beacon_message(message, host)
            self._process_beacon(beacon)

    def _process_beacon(self, beacon):
        print repr(beacon)
        if beacon.identity != self.identity:
            peer = self._get_or_create_peer(beacon.host, beacon.port, beacon.identity)
            self._reset_peer_heartbeat(peer)

    def _get_or_create_peer(self, host, port, identity):
        try:
            peer = self.peer_map[identity]
        except KeyError:
            peer = self.peer_map[identity] = self._create_peer(host, port, identity)
        return peer

    def _create_peer(self, host, port, identity):
        dealer = self._create_dealer(host, port, identity)
        beacon_message = dealer.encode_message_str(self.zmq_beacon_message)
        peer = self.peer_factory(identity, dealer)
        peer.heartbeat = self.reactor.create_looping_call(peer.dealer.send, beacon_message)
        peer.heartbeat.start(self.protocol.zmq_heartbeat_interval)
        return peer

    def _create_dealer(self, host, port, identity):
        dealer = self.peer_map[identity] = self.zmq_socket_factory.create_dealer_socket(identity)
        dealer.sndhwm = self.protocol.zmq_heartbeat_interval * 100
        dealer.sndtimeo = 0
        dealer.message_received.connect(partial(self._process_dealer_message, identity))
        dealer.start(host, port)
        self.dealer_created.emit(identity, dealer)
        return dealer

    def _process_dealer_message(self, identity, message):
        peer = self.peer_map[identity]
        self._reset_peer_heartbeat(peer)

    @staticmethod
    def _reset_peer_heartbeat(peer):
        peer.heartbeat.reset()


class AgentFactory(object):
    reactor = ReactorInterface
    udp_host = None
    udp_port = None
    protocol = None
    broadcast_factory = None
    peer_factory = Peer

    def __init__(self, zmq_socket_factory):
        self.zmq_socket_factory = zmq_socket_factory

    def __call__(self, identity, config):
        instance = Agent(identity, config)
        instance.reactor = self.reactor
        instance.protocol = self.protocol
        instance.zmq_socket_factory = self.zmq_socket_factory
        instance.broadcast = self._create_broadcast()
        instance.peer_factory = self.peer_factory
        return instance

    def _create_broadcast(self):
        instance = self.broadcast_factory()
        instance.reactor = self.reactor
        return instance
