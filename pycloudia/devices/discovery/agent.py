from pysigslot import Signal

from pycloudia.reactor.interfaces import ReactorInterface


class Peer(object):
    heartbeat = None

    def __init__(self, identity, push):
        self.identity = identity
        self.push = push


class Agent(object):
    reactor = ReactorInterface
    protocol = None
    broadcast = None
    zmq_stream_factory = None
    peer_factory = None

    def __init__(self, config):
        self.config = config

        self.push_created = Signal()
        self.push_deleted = Signal()

        self.sink = None
        self.heartbeat = None
        self.udp_beacon_message = None
        self.zmq_beacon_message = None

        self.peer_map = {}

    def start(self):
        port = self._start_sink()
        self._create_beacons(port)
        self._start_broadcast()
        self._start_heartbeat()

    def _start_sink(self):
        self.sink = self.zmq_stream_factory.create_sink_stream()
        self.sink.message_received.connect(self._process_sink_message)
        return self.sink.start_on_random_port(self.config.host, self.config.min_port, self.config.max_port)

    def _create_beacons(self, port):
        self.udp_beacon_message = self.protocol.create_udp_beacon_message(self.config.host, port, self.config.identity)
        self.zmq_beacon_message = self.protocol.create_zmq_beacon_message(self.config.host, port, self.config.identity)

    def _start_broadcast(self):
        self.broadcast.message_received.connect(self._process_broadcast_message)
        self.broadcast.start()

    def _start_heartbeat(self):
        self.heartbeat = self.reactor.create_looping_call(self.broadcast.send_message, self.udp_beacon_message)
        self.heartbeat.start(self.protocol.udp_heartbeat_interval)

    def _process_sink_message(self, message):
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
        if beacon.identity != self.config.identity:
            peer = self._get_or_create_peer(beacon.host, beacon.port, beacon.identity)
            self._reset_peer_heartbeat(peer)

    def _get_or_create_peer(self, host, port, identity):
        try:
            peer = self.peer_map[identity]
        except KeyError:
            peer = self.peer_map[identity] = self._create_peer(host, port, identity)
        return peer

    def _create_peer(self, host, port, identity):
        push = self._create_push(host, port, identity)
        beacon_message = push.encode_message_str(self.zmq_beacon_message)
        peer = self.peer_factory(identity, push)
        peer.heartbeat = self.reactor.create_looping_call(peer.push.send_message, beacon_message)
        peer.heartbeat.start(self.protocol.zmq_heartbeat_interval)
        return peer

    def _create_push(self, host, port, identity):
        push = self.peer_map[identity] = self.zmq_stream_factory.create_push_stream(self.config.identity)
        push.sndhwm = self.protocol.zmq_heartbeat_interval * 100
        push.sndtimeo = 0
        push.start(host, port)
        self.push_created.emit(identity, push)
        return push

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

    def __init__(self, zmq_stream_factory):
        self.zmq_stream_factory = zmq_stream_factory

    def __call__(self, config):
        instance = Agent(config)
        instance.reactor = self.reactor
        instance.protocol = self.protocol
        instance.zmq_stream_factory = self.zmq_stream_factory
        instance.broadcast = self._create_broadcast()
        instance.peer_factory = self.peer_factory
        return instance

    def _create_broadcast(self):
        instance = self.broadcast_factory()
        instance.reactor = self.reactor
        return instance
