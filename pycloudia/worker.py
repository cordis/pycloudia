from collections import namedtuple
from pycloudia.uitls.defer import inline_callbacks


WorkerOptions = namedtuple('WorkerOptions', 'zmq udp interface cluster groups')


class Worker(object):
    reactor = None
    console = None

    def __init__(self, options):
        self.options = options

    def initialize(self):
        self.reactor.register_for_shutdown(self._shutdown)

    def run(self):
        self.reactor.call_when_running(self._run)
        self.reactor.run()

    @inline_callbacks
    def _run(self):
        raise NotImplementedError()

    def _shutdown(self):
        raise NotImplementedError()
