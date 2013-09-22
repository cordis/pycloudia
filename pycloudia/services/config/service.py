from pycloudia.defer import inline_callbacks, return_value
from pycloudia.channels.declarative import respond, publish
from pycloudia.channels.consts import IMPL
from pycloudia.services.config.consts import CHANNEL


class Service(object):
    state = None
    request_factory = None
    processor_factory = None

    @respond(CHANNEL.WORKERS)
    @inline_callbacks
    def process_worker_request(self, package):
        request = self.request_factory(package)
        processor = self.processor_factory(request)
        response = yield processor.process(self.state, request)
        return_value(response)

    @publish(CHANNEL.WORKERS)
    def publish_worker_event(self, package):
        return package

    @respond(CHANNEL.MANAGERS, impl=IMPL.HTTP, port=443)
    @inline_callbacks
    def process_manage_request(self, package):
        # @TODO: authentication
        pass


class ServiceFactory(object):
    state_factory = None
    request_factory = None
    processor_factory = None

    def __call__(self):
        instance = Service()
        instance.state = self.state_factory()
        instance.request_factory = self.request_factory
        instance.processor_factory = self.processor_factory
        return instance
