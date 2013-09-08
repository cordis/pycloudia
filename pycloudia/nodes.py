from pycloudia.channels.registry import ChannelsRegistry
from pycloudia.services.registry import ServicesRegistry
from pycloudia.defer import inline_callbacks


class BaseNode(object):
    reactor = None

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        raise NotImplementedError()


class WorkerNode(BaseNode):
    config = None
    channels = {}
    services = {}

    @inline_callbacks
    def run(self):
        channels_config = yield self.config.get_channels()
        self.channels = self._configure_channels(channels_config)
        services_config = yield self.config.get_services()
        self.services = self._configure_services(self.channels, services_config)
        yield self.channels.run()
        yield self.services.run()

    def _configure_channels(self, channels_config):
        registry = ChannelsRegistry()
        registry.configure(channels_config.get_bean_list())
        return registry

    def _configure_services(self, channels, services_config):
        registry = ServicesRegistry(self.config, channels)
        registry.configure(services_config.get_bean_list())
        return registry
