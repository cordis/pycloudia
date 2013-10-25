from pycloudia.uitls.defer import inline_callbacks
from pycloudia.uitls.net import get_ip_address


class Worker(object):
    reactor = None
    console = None

    def __init__(self, port, interface='eth0', group=None, roles=None):
        self.port = port
        self.host = get_ip_address(interface)
        self.group = group
        self.roles = roles or []
#        self.cluster = Cluster(options)
#        self.threads = Threads()

    def run(self):
        self.reactor.register_for_shutdown(self._shutdown)
        self.reactor.call_when_running(self._run)
        self.reactor.run()

    @inline_callbacks
    def _run(self):
        raise NotImplementedError()

    def _shutdown(self):
        raise NotImplementedError()
