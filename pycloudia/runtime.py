from collections import namedtuple
from logging import getLogger
from inspect import getmembers
from itertools import ifilter, imap
from operator import itemgetter
from time import time

from pycloudia.channels.address import Address
from pycloudia.uitls.decorators import generate_list
from pycloudia.uitls.defer import inline_callbacks, maybe_deferred
from pycloudia.channels.declarative import ChannelDeclaration
from pycloudia.services.config import CHANNEL


ServiceIdentity = namedtuple('BaseServiceIdentity', 'cls identity')
ChannelIdentity = namedtuple('BaseServiceChannel', 'service_identity channel_name channel_method')


class Runtime(object):
    logger = getLogger('pycloudia.runtime')
    reactor = None

    identity = None

    socket_factory_registry = None
    channel_factory = None

    def __init__(self, options):
        self.options = options
        self.services = {}
        self.channels = {}
        self.config_endpoint_list = ConfigAddressList(self.options)

    def set_identity(self, identity):
        self.identity = identity

    def install_config_service(self, service):
        service_identity = self._create_service_identity(service)
        workers_channel_declaration = self._get_channel_declaration_by_name(service, CHANNEL.CONFIG)
        channel_pool = self._get_or_run_channel_pool(service_identity, workers_channel_declaration)
        channel_pool.extend_endpoints(self.config_endpoint_list.get_local())
        replicas_channel_declaration = self._get_channel_declaration_by_name(service, CHANNEL.CONFIG)
        channel_pool = self._get_or_run_channel_pool(service, replicas_channel_declaration)
        channel_pool.extend_endpoints(*self.config_endpoint_list.get_remotes())
        return self.run_service(service)

    def install_worker_service(self, service):
        config_channel_declaration = self._get_channel_declaration_by_name(service, CHANNEL.CONFIG)
        channel_pool = self._get_or_run_channel_pool(service, config_channel_declaration)
        channel_pool.extend_endpoints(self.config_endpoint_list.get_all())
        return self.run_service(service)

    def _get_channel_declaration_by_name(self, service, channel_declaration_name):
        for channel_declaration in self._extract_service_channel_declarations(service):
            if channel_declaration.options.name == channel_declaration_name:
                return channel_declaration
        raise KeyError('Config channel not found in service')

    def _create_service_identity(self, service, identity=None):
        return ServiceIdentity(type(service), identity)

    def _get_or_run_channel_pool(self, service_identity, channel_declaration):
        channel_identity = self._create_channel_identity(service_identity, channel_declaration)
        try:
            return self.channels[channel_identity]
        except KeyError:
            channel_pool = self.channels[channel_identity] = self._create_channel_pool(channel_declaration)
            channel_pool.run()
            return channel_pool

    def _create_channel_identity(self, service_identity, channel_declaration):
        return ChannelIdentity(service_identity, channel_declaration.name, channel_declaration.method)

    def _create_channel_pool(self, channel_declaration):
        raise NotImplementedError()

    # -----------------------------------------------------------------------------------------------------------------

    @inline_callbacks
    def install_service(self, service):
        for method_name, channel_declaration in self._extract_service_channel_declarations(service):
            self.install_channel_declaration(channel_declaration)

    def _extract_service_channel_declarations(self, service):
        members = imap(itemgetter('1'), getmembers(service))
        return ifilter(self._is_channel_method, members)

    def _is_channel_method(self, member):
        return callable(member) and isinstance(member, ChannelDeclaration)

    def install_channel_declaration(self, channel_declaration):
        self.channels[channel_declaration.name] = channel_declaration

    def run_channel(self, channel_name, address=None):
        channel_declaration = self.channels[channel_name]
        channel, created = self._get_or_create_channel(channel_declaration, address)
        channel_declaration.add_handler(channel.get_handler())
        if created:
            channel.run()

    def _get_or_create_channel(self, channel_declaration, address):
        socket_factory = self._get_socket_factory(channel_declaration)
        socket = socket_factory(channel_declaration.name, channel_declaration.method, address.host, address.port)
        return self.channel_factory(socket), True

    def _get_socket_factory(self, channel_declaration):
        return self.socket_factory_registry[channel_declaration.impl]

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


class ConfigAddressList(object):
    def __init__(self, options):
        self.options = options

    def get_remotes(self):
        return set(self.get_all()) - {self.get_local()}

    def get_local(self):
        for address in self.get_all():
            if address.host in (self.options.internal_host, self.options.external_host):
                return address
        else:
            raise KeyError('No one of config addresses matches localhost')

    @generate_list
    def get_all(self):
        for address_string in self.options.config_address_list:
            yield Address.from_string(address_string)
