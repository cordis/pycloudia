from pycloudia.channels.channel import PullChannel
from pycloudia.channels.registry import ChannelsRegistry
from pycloudia.services.registry import ServicesRegistry
from pycloudia.defer import inline_callbacks
from pycloudia.utils import import_class


class BaseNode(object):
    reactor = None
    shell = None

    def bind_shell(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def _create_channel_factory(self, path):
        channel_factory_cls = import_class(path)
        return channel_factory_cls()


class WorkerNode(BaseNode):
    config = None

    def __init__(self):
        self.channels = {}
        self.services = {}

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


class ConfigNode(BaseNode):
    def __init__(self, cluster_config, services_config, machine_name, port):
        self.cluster_config = cluster_config
        self.services_config = services_config
        self.machine_name = machine_name
        self.port = port
        self.channel = None
        self.service = None

    @inline_callbacks
    def run(self):
        self.channel = self._create_channel()
        yield self.channel.run()
        self.service = self._create_config_service(self.channel)
        yield self.service.run()

    def _create_channel(self):
        host = self.cluster_config.get_host_by_machine_name(self.machine_name)
        channel_factory = self._create_channel_factory(self.services_config.get_channels_factory_path())
        return channel_factory.create_pull_channel(host, self.port)

    def _create_config_service(self, channel):
        return None
