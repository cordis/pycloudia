from pycloudia.utils import import_class
from pycloudia.channels.channel import PullChannel, PushChannel
from pycloudia.packages.factory import PackageFactory
from pycloudia.packages.decoder import PackageDecoder
from pycloudia.packages.encoder import PackageEncoder


class ChannelsFactory(object):
    package_factory = PackageFactory()
    package_decoder = PackageDecoder()
    package_encoder = PackageEncoder()

    def __init__(self, default_router_path=None, default_socket_factory_path=None):
        self.default_socket_factory_path = default_socket_factory_path
        self.default_router_path = default_router_path

    def create_pull_channel(self, name, router_path=None, socket_factory_path=None, **kwargs):
        channel = PullChannel(name, self._get_router(router_path))
        return self._inject_implementation(channel, socket_factory_path, **kwargs)

    def create_push_channel(self, name, router_path=None, socket_factory_path=None, **kwargs):
        channel = PushChannel(name, self._get_router(router_path))
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
