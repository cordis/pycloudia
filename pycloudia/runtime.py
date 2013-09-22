from inspect import getmembers
from itertools import ifilter

from pycloudia.defer import inline_callbacks
from pycloudia.channels.declarative import ChannelDecorator


class Runtime(object):
    socket_factory_registry = None
    channel_factory = None

    def __init__(self, options):
        self.options = options
        self.channel_handlers = {}

    @inline_callbacks
    def install_config_service(self, service):
        for method_name, channel_decorator in self._extract_service_channel_decorators(service):
            self.install_channel_decorator(channel_decorator)

    @inline_callbacks
    def install_worker_service(self, service):
        pass

    @inline_callbacks
    def install_service(self, service):
        pass

    def _extract_service_channel_decorators(self, service):
        return ifilter(self._is_channel_method, getmembers(service))

    def _is_channel_method(self, member):
        return callable(member) and isinstance(member, ChannelDecorator)

    def install_channel_decorator(self, channel_decorator):
        for channel in self._get_or_create_channels(channel_decorator):
            channel_decorator.add_handler(channel.get_handler())
            channel.run()

    def _get_or_create_channels(self, channel_decorator):
        socket_factory = self._get_socket_factory(channel_decorator)
        if channel_decorator.internal:
            yield self._create_channel(self.options.internal_host, channel_decorator, socket_factory)
        if channel_decorator.external:
            yield self._create_channel(self.options.external_host, channel_decorator, socket_factory)

    def _create_channel(self, host, channel_decorator, socket_factory):
        return self.channel_factory(
            socket_factory,
            channel_decorator.method,
            channel_decorator.name,
            channel_decorator.port,
            host
        )

    def _get_socket_factory(self, channel_decorator):
        return self.socket_factory_registry[channel_decorator.impl]
