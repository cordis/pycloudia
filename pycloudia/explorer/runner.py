from pysigslot import Signal

from pycloudia.reactor.interfaces import ReactorInterface
from pycloudia.explorer.beans import Peer


class Runner(object):
    reactor = ReactorInterface
    logger = None
    protocol = None
    broadcast = None
    stream_factory = None

    def __init__(self, config):
        self.config = config

        self.incoming_stream_created = Signal()
        self.outgoing_stream_created = Signal()
        self.outgoing_stream_deleted = Signal()

        self.sink = None
        self.heartbeat = None
        self.broadcast_beacon_message = None
        self.immediate_beacon_message = None

        self.peer_map = {}

    def start(self):
        port = self._start_sink()
        self._create_beacons(port)
        self._start_broadcast()
        self._start_heartbeat()

    def _start_sink(self):
        self.sink = self.stream_factory.create_sink_stream()
        self.sink.message_received.connect(self._process_sink_message)
        return self.sink.start_on_random_port(self.config.host, self.config.min_port, self.config.max_port)

    def _create_beacons(self, port):
        self.broadcast_beacon_message = self._create_broadcast_beacon_message(port)
        self.immediate_beacon_message = self._create_immediate_beacon_message(port)

    def _create_broadcast_beacon_message(self, port):
        return self.protocol.create_broadcast_beacon_message(self.config.host, port, self.config.identity)

    def _create_immediate_beacon_message(self, port):
        return self.protocol.create_immediate_beacon_message(self.config.host, port, self.config.identity)

    def _start_broadcast(self):
        self.broadcast.message_received.connect(self._process_broadcast_message)
        self.broadcast.start()

    def _start_heartbeat(self):
        self.heartbeat = self.reactor.create_looping_call(self.broadcast.send_message, self.broadcast_beacon_message)
        self.heartbeat.start(self.protocol.broadcast_heartbeat_interval)

    def _process_sink_message(self, message):
        try:
            peer = self.peer_map[message.peer]
            self._reset_peer_heartbeat(peer)
        except KeyError:
            assert self.protocol.is_beacon(message)
            beacon = self.protocol.parse_immediate_beacon_message(message, message.peer)
            self._process_beacon(beacon)

    def _process_broadcast_message(self, message, host):
        if self.protocol.is_beacon(message):
            beacon = self.protocol.parse_broadcast_beacon_message(message, host)
            self._process_beacon(beacon)

    def _process_beacon(self, beacon):
        print beacon
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
        stream = self._create_push_stream(host, port, identity)
        beacon_message = stream.encode_message_string(self.immediate_beacon_message)
        heartbeat = self.reactor.create_looping_call(stream.send_message, beacon_message)
        heartbeat.start(self.protocol.immediate_heartbeat_interval)
        return Peer(identity=identity, stream=stream, heartbeat=heartbeat)

    def _create_push_stream(self, host, port, identity):
        push = self.peer_map[identity] = self.stream_factory.create_push_stream(self.config.identity)
        push.sndhwm = self.protocol.immediate_heartbeat_interval * 100
        push.sndtimeo = 0
        push.start(host, port)
        self.outgoing_stream_created.emit(identity, push)
        return push

    @staticmethod
    def _reset_peer_heartbeat(peer):
        peer.heartbeat.reset()


class RunnerFactory(object):
    logger = None
    reactor = ReactorInterface
    protocol = None
    broadcast_factory = None

    def __init__(self, stream_factory):
        self.stream_factory = stream_factory

    def __call__(self, config):
        instance = Runner(config)
        instance.logger = self.logger
        instance.reactor = self.reactor
        instance.protocol = self.protocol
        instance.stream_factory = self.stream_factory
        instance.broadcast = self._create_broadcast()
        return instance

    def _create_broadcast(self):
        instance = self.broadcast_factory()
        instance.reactor = self.reactor
        return instance
