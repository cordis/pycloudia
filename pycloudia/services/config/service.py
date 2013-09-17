from pycloudia.defer import inline_callbacks, return_value
from pycloudia.parsers.factory import ParserFactory
from pycloudia.services.config.schemas import ClustersConfigSchema, ChannelsConfigSchema
from pycloudia.services.config.requests import RequestsFactory
from pycloudia.services.config.processors import ProcessorsFactory
from pycloudia.services.config.states import ConfigState


class ConfigService(object):
    state = None
    request_factory = None
    processor_factory = None

    def run(self):
        pass

    @inline_callbacks
    def process_worker_request(self, package):
        request = self.request_factory(package)
        processor = self.processor_factory(request)
        response = yield processor.process(request)
        return_value(response)

    @inline_callbacks
    def process_manage_request(self, package):
        # @TODO: authentication
        pass


class ConfigServiceFactory(object):
    config_parser_factory = ParserFactory()

    def __init__(self, clusters_filename, channels_filename, services_filename):
        self.clusters_config = self._get_clusters_config(clusters_filename)
        self.channels_config = self._get_channels_config(channels_filename)
        self.services_config = self._get_services_config(services_filename)

    def __call__(self):
        instance = ConfigService()
        instance.state = state = self._create_state()
        instance.request_factory = RequestsFactory()
        instance.processor_factory = ProcessorsFactory(state)
        return instance

    def _create_state(self):
        instance = ConfigState()
        return instance

    def _get_clusters_config(self, filename):
        return ClustersConfigSchema().decode(self._load_config(filename))

    def _get_channels_config(self, filename):
        return ChannelsConfigSchema().decode(self._load_config(filename))

    def _load_config(self, filename):
        return self.config_parser_factory(filename).load()
