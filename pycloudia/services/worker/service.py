from pycloudia.uitls.defer import inline_callbacks, maybe_deferred
from pycloudia.channels.declarative import dealer
from pycloudia.services import config
from pycloudia.services.worker.messages import InitMessage, PingMessage


class Service(object):
    reactor = None
    request_factory = None
    response_factory = None
    processor_factory = None

    config = dealer(config.CHANNEL.WORKERS)

    def __init__(self, runtime):
        self.runtime = runtime
        self.worker_id = None
        self.ping = None

    @inline_callbacks
    def initialize(self):
        package = yield self.send_config_message(self._create_init_message())
        response = self.response_factory(package)
        self.runtime.set_identity(response.worker_id)
        self.ping.set_message(self._create_ping_message())

    def _create_init_message(self):
        return InitMessage(
            self.runtime.options.internal_host,
            self.runtime.options.extrenal_host
        )

    def _create_ping_message(self):
        return PingMessage()

    @config.broadcast
    def send_config_message(self, package):
        pass

    @config.consume
    @inline_callbacks
    def process_config_message(self, package):
        request = self.request_factory(package)
        processor = self.processor_factory(self, request)
        yield self.reactor.call(processor.process)

    @inline_callbacks
    def run(self):
        yield maybe_deferred(self.ping.start)

    @inline_callbacks
    def shutdown(self):
        yield maybe_deferred(self.ping.stop)
