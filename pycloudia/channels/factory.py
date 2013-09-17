from pycloudia.uitls.code import import_class, instantiate_by_config
from pycloudia.packages.factory import PackageFactory
from pycloudia.packages.decoder import PackageDecoder
from pycloudia.packages.encoder import PackageEncoder
from pycloudia.channels.responder import Responder
from pycloudia.channels.channel import PullChannel, PushChannel


class ChannelFactory(object):
    responder_factory = Responder
    push_channel_factory = PushChannel
    pull_channel_factory = PullChannel
    package_factory = PackageFactory()
    package_decoder = PackageDecoder()
    package_encoder = PackageEncoder()

    def __init__(self, reactor, localhost):
        self.reactor = reactor
        self.localhost = localhost
        self.responder = self._create_responder(self.reactor)

    def _create_responder(self, reactor):
        responder = self.responder_factory()
        responder.reactor = reactor
        return responder

    def create_pull_channel(self, name, config):
        channel = self.pull_channel_factory(name, self._get_router(router_path))
        return self._inject_implementation(channel, socket_factory_path, **kwargs)

    def create_push_channel(self, name, config):
        channel = self.push_channel_factory(name, self._get_router(router_path))
        return self._inject_implementation(channel, socket_factory_path, **kwargs)

    def _get_router(self, router_path):
        if router_path is None:
            router_path = self.default_router_path
        router_cls = import_class(router_path)
        return router_cls()

    def _inject_implementation(self, channel, socket_factory_path, **kwargs):
        self._get_socket_factory(socket_factory_path).inject_implementation(channel, **kwargs)
        channel.package_decoder = self.package_decoder
        channel.package_encoder = self.package_encoder
        return channel

    def _get_socket_factory(self, socket_factory_path):
        if socket_factory_path is None:
            socket_factory_path = self.default_socket_factory_path
        socket_factory_cls = import_class(socket_factory_path)
        return socket_factory_cls()


class ChannelFactoryBuilder(object):
    channel_factory_cls = ChannelFactory
    package_factory_cls = PackageFactory
    package_decoder_cls = PackageDecoder
    package_encoder_cls = PackageEncoder

    def __init__(self, reactor, localhost):
        self.reactor = reactor
        self.localhost = localhost

    def build(self, config=None):
        channel_factory = self._instantiate_channel_factory(config)
        channel_factory.package_factory = self._instantiate_package_factory(config or {})
        channel_factory.package_decoder = self._instantiate_package_decoder(config or {})
        channel_factory.package_encoder = self._instantiate_package_decoder(config or {})
        return channel_factory

    def _instantiate_channel_factory(self, config):
        def factory(cls, **kwargs):
            return cls(self.reactor, self.localhost, **kwargs)
        return instantiate_by_config(self.channel_factory_cls, config, factory)

    def _instantiate_package_factory(self, config):
        return instantiate_by_config(self.package_factory_cls, config.get('package_factory', None))

    def _instantiate_package_decoder(self, config):
        return instantiate_by_config(self.package_decoder_cls, config.get('package_decoder', None))

    def _instantiate_package_encoder(self, config):
        return instantiate_by_config(self.package_encoder_cls, config.get('package_encoder', None))
