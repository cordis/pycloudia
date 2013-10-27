from collections import namedtuple

from twisted.internet.protocol import DatagramProtocol

from pycloudia.devices.consts import DEVICE
from pycloudia.reactor.interfaces import ReactorInterface
from pycloudia.uitls.defer import inline_callbacks, maybe_deferred, Deferred, deferrable


class Device(object):
    reactor = ReactorInterface()
    console = None

    def __init__(self, host, port, group=None, roles=None):
        self.host = host
        self.port = port
        self.group = group
        self.roles = roles or []
#        self.cluster = Cluster(options)
#        self.threads = Threads()

    def initialize(self):
        self.reactor.call_when_running(self._run)
        self.reactor.register_for_shutdown(self._shutdown)

    @inline_callbacks
    def _run(self):
        yield self._create_discovery().start()

    def _create_discovery(self):
        protocol = DiscoveryUdpProtocol(self)
        protocol.reactor = self.reactor
        return protocol

    def _shutdown(self):
        raise NotImplementedError()


