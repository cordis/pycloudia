from pycloudia.defer import inline_callbacks
from pycloudia.channels.declarative import request, subscribe
from pycloudia.services import config
from pycloudia.services.worker.messages import OnlineMessage
from pycloudia.services.worker.schemas import ConfigSubscriptionSchema


class Service(object):
    request_factory = None
    processor_factory = None

    def __init__(self, runtime):
        self.runtime = runtime

    @inline_callbacks
    def initialize(self):
        package = yield self.get_config_subscription()
        self.subscribe_for_updates(package)

    @request(config.CHANNEL.WORKERS)
    def get_config_subscription(self):
        return OnlineMessage(self.runtime.options.internal_host, self.runtime.options.extrenal_host)

    def _create_online_request_package(self):
        pass

    def subscribe_for_updates(self, package):
        subscription = ConfigSubscriptionSchema().decode(package.get_content())
        for channel in subscription.channels:
            channel_decorator_factory = self._create_subscribe_channel_decorator_factory(channel)
            self.process_update = channel_decorator_factory(self.process_update)
        self.runtime.install_channel_decorator(self.process_update)

    def _create_subscribe_channel_decorator_factory(self, channel):
        return subscribe(channel.name, host=channel.host, port=channel.port, topic=channel.topic)

    def process_update(self, package):
        pass

