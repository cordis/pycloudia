from uuid import uuid1

from pycloudia.reactor.interfaces import ReactorInterface
from pycloudia.uitls.defer import inline_callbacks
from pycloudia.devices.discovery.director import DiscoveryDirector


class Device(object):
    identity_factory = uuid1

    reactor = ReactorInterface()
    console = None

    def __init__(self, address, group=None, roles=None):
        self.address = address
        self.group = group
        self.roles = roles or []
        self.identity = self.identity_factory()
#        self.cluster = Cluster(options)
#        self.threads = Threads()

    def initialize(self):
        self.reactor.call_when_running(self._run)
        self.reactor.register_for_shutdown(self._shutdown)

    @inline_callbacks
    def _run(self):
        yield self._create_discoverer().start()

    def _create_discoverer(self):
        discoverer = DiscoveryDirector(self.identity, self.address)
        discoverer.reactor = self.reactor
        return discoverer

    def _shutdown(self):
        raise NotImplementedError()
