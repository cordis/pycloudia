from pycloudia.defer import inline_callbacks, return_value
from pycloudia.services.config.requests import RequestsFactory
from pycloudia.services.config.processors import ProcessorsFactory


class ConfigService(object):
    def __init__(self, cluster_config, services_config):
        self.cluster_config = cluster_config
        self.services_config = services_config
        self.request_factory = RequestsFactory()
        self.processor_factory = ProcessorsFactory(self._create_state())

    def _create_state(self):
        pass

    def run(self):
        pass

    @inline_callbacks
    def process_request(self, package):
        request = self.request_factory(package)
        processor = self.processor_factory(request)
        response = yield processor.process(request)
        return_value(response)
