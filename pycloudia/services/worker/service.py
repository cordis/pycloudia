from pycloudia.defer import inline_callbacks
from pycloudia.channels.declarative import dealer
from pycloudia.services import config
from pycloudia.services.worker.messages import OnlineMessage


class Service(object):
    worker_id = None
    request_factory = None
    processor_factory = None

    config = dealer(config.CHANNEL.WORKERS)

    def __init__(self, runtime):
        self.runtime = runtime

    @inline_callbacks
    def initialize(self):
        yield self.get_config_subscription(self._create_online_message())

    def _create_online_message(self):
        return OnlineMessage(
            self.worker_id,
            self.runtime.options.internal_host,
            self.runtime.options.extrenal_host
        )

    @config.broadcast
    def get_config_subscription(self, package):
        pass

    @config.listen
    def process_config_message(self, package):
        pass
