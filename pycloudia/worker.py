from pycloudia.uitls.defer import inline_callbacks


class Worker(object):
    reactor = None
    console = None

    def __init__(self, host, port, group=None, roles=None):
        self.host = host
        self.port = port
        self.group = group
        self.roles = roles or []
#        self.cluster = Cluster(options)
#        self.threads = Threads()

    def setup(self):
        self.reactor.register_for_shutdown(self._shutdown)
        self.reactor.call_when_running(self._run)

    @inline_callbacks
    def _run(self):
        raise NotImplementedError()

    def _shutdown(self):
        raise NotImplementedError()
