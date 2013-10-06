from pycloudia.channels.channels import Channel
from pycloudia.packages.decoder import PackageDecoder
from pycloudia.packages.encoder import PackageEncoder


class ChannelFactory(object):
    channel_cls = Channel
    package_decoder = PackageDecoder
    package_encoder = PackageEncoder

    def __init__(self, options):
        self.options = options

    def __call__(self, socket_factory, socket_method, channel_name, host, port):
        socket = socket_factory(socket_method, host, port)
        return self.channel_cls(channel_name, socket)

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
