from logging import getLogger
from inspect import getmembers
from itertools import ifilter, imap
from operator import itemgetter
from time import time

from pycloudia.channels.address import Address
from pycloudia.decorators import generate_list
from pycloudia.defer import inline_callbacks, maybe_deferred
from pycloudia.channels.declarative import ChannelDecorator
from pycloudia.services.config import CHANNEL


class Runtime(object):
    logger = getLogger('pycloudia.runtime')

    socket_factory_registry = None
    channel_factory = None

    def __init__(self, options):
        self.options = options
        self.channel_decorator_map = {}

    def install_config_service(self, service):
        worker_request_channel_decorator = self._get_config_channel_decorator(service)
        self.install_channel_decorator(worker_request_channel_decorator)
        for address in self._get_config_address_list():
            if address.host in (self.options.internal_host, self.options.external_host):
                self.run_channel(worker_request_channel_decorator.channel_name, address)
                break
        else:
            raise KeyError('No one of config addresses matches localhost')
        return self.run_service(service)

    def install_worker_service(self, service):
        config_request_channel_decorator = self._get_config_channel_decorator(service)
        self.install_channel_decorator(config_request_channel_decorator)
        for address in self._get_config_address_list():
            self.run_channel(config_request_channel_decorator.channel_name, address)
        return self.run_service(service)

    def _get_config_channel_decorator(self, service):
        for channel_decorator in self._extract_service_channel_decorators(service):
            if channel_decorator.options.name == CHANNEL.WORKERS:
                return channel_decorator
        raise KeyError('Config channel not found in service')

    @generate_list
    def _get_config_address_list(self):
        for address_string in self.options.config_address_list:
            yield Address.from_string(address_string)

    @inline_callbacks
    def install_service(self, service):
        for method_name, channel_decorator in self._extract_service_channel_decorators(service):
            self.install_channel_decorator(channel_decorator)

    def _extract_service_channel_decorators(self, service):
        members = imap(itemgetter('1'), getmembers(service))
        return ifilter(self._is_channel_method, members)

    def _is_channel_method(self, member):
        return callable(member) and isinstance(member, ChannelDecorator)

    def install_channel_decorator(self, channel_decorator):
        self.channel_decorator_map[channel_decorator.name] = channel_decorator

    def run_channel(self, channel_name, address=None):
        channel_decorator = self.channel_decorator_map[channel_name]
        channel, created = self._get_or_create_channel(channel_decorator, address)
        channel_decorator.add_handler(channel.get_handler())
        if created:
            channel.run()

    def _get_or_create_channel(self, channel_decorator, address):
        socket_factory = self._get_socket_factory(channel_decorator)
        socket = socket_factory(channel_decorator.name, channel_decorator.method, address.host, address.port)
        return self.channel_factory(socket), True

    def _get_socket_factory(self, channel_decorator):
        return self.socket_factory_registry[channel_decorator.impl]

    @inline_callbacks
    def run_service(self, service):
        start = time()
        try:
            yield maybe_deferred(service.initialize)
            yield maybe_deferred(service.run)
        except RuntimeError as e:
            self._log_service_failure(service, e)
        else:
            self._log_service_success(service, time() - start)

    def _log_service_failure(self, service, exception):
        self.logger.error(
            'Channel %s has not been started on %s:%s: %s',
            service.name,
            service.host,
            service.port,
            exception
        )

    def _log_service_success(self, service, start_duration):
        self.logger.info(
            'Channel %s started on %s:%s in %.3f seconds',
            service.name,
            service.host,
            service.port,
            start_duration
        )
