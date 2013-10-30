from pycloudia.reactor.interfaces import ReactorInterface
from pycloudia.uitls.defer import inline_callbacks, Deferred, deferrable
from pycloudia.channels import METHOD
from pycloudia.channels.txzmq_impl import SocketFactory
from pycloudia.devices.consts import DEVICE
from pycloudia.devices.discovery.udp import DiscoveryUdpProtocol


class DiscoveryDirector(object):
    reactor = ReactorInterface()
    multicast_factory = DiscoveryUdpProtocol
    heartbeat_interval = DEVICE.UDP.HEARTBEAT_INTERVAL
    zmq_socket_factory = SocketFactory()

    def __init__(self, identity, address, interface=''):
        self.identity = identity
        self.address = address
        self.interface = interface
        self.multicast = None
        self.heartbeat = None
        self.router = None
        self.peers = {}

    @inline_callbacks
    def start(self):
        yield self._start_router()
        yield self._start_multicast()
        yield self._start_heartbeat()

    def _start_router(self):
        self.router = self.zmq_socket_factory(METHOD.ROUTER, self.address, identity=self.identity)
        self.router.start(self._process_router_message)

    def _start_multicast(self):
        deferred = Deferred()
        self.multicast = self.multicast_factory(self._process_multicast_message)
        self.multicast.set_start_callback(deferred.callback)
        self.reactor.call_feature(
            'listenMulticast',
            self.multicast.address.port,
            self.multicast,
            self.interface,
            listenMultiple=True
        )
        return deferred

    @deferrable
    def _start_heartbeat(self):
        self.heartbeat = self.reactor.create_looping_call(self._send_heartbeat)
        self.heartbeat.start(self.heartbeat_interval)

    def _send_heartbeat(self):
        self.multicast.send('BEACON')

    def _process_router_message(self, message):
        hops = message.hops
        peer = message.peer

    def _process_multicast_message(self, message, host):
        pass
