from pycloudia.utils.defer import inline_callbacks


class WorkerNode(object):
    reactor = None
    console = None
    runtime_factory = None
    worker_service_factory = None

    def __init__(self, options):
        self.options = options
        self.runtime = None

    def initialize(self):
        self.runtime = self.runtime_factory()
        self.reactor.register_for_shutdown(self._shutdown)

    def run(self):
        self.reactor.call_when_running(self._run)
        self.reactor.run()

    @inline_callbacks
    def _run(self):
        yield self.runtime.install_worker_service(self.worker_service_factory(self.runtime))

    def _shutdown(self):
        raise NotImplementedError()


class ConfigNode(WorkerNode):
    config_service_factory = None

    @inline_callbacks
    def _run(self):
        yield self.runtime.install_config_service(self.config_service_factory())
        yield super(ConfigNode, self)._run()
