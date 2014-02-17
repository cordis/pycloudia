from uuid import uuid1

from pycloudia.reactor.interfaces import IReactor
from pycloudia.utils.defer import inline_callbacks
from pycloudia.explorer.runner import Runner


class Device(object):
    identity_factory = uuid1

    reactor = IReactor()
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
        yield self.reactor.call_later(15, self._start_activities)

    def _create_discoverer(self):
        discoverer = Runner(self.identity, self.address)
        discoverer.reactor = self.reactor
        return discoverer

    def _shutdown(self):
        raise NotImplementedError()

    def _start_activities(self):
        pass
