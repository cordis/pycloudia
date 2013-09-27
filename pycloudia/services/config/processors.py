from pycloudia.defer import deferrable
from pycloudia.services.config.requests import PingRequest, InitRequest
from pycloudia.services.config.messages import PingResponse, InitResponse


class BaseProcessor(object):
    def __init__(self, service, request):
        self.service = service
        self.request = request

    @deferrable
    def process(self, worker_id):
        raise NotImplementedError()


class PingProcessor(BaseProcessor):
    @deferrable
    def process(self, worker_id):
        self.service.ping_worker(worker_id, self.request.timestamp)
        return PingResponse()


class InitProcessor(BaseProcessor):
    @deferrable
    def process(self, worker_id):
        self.service.init_worker(worker_id, self.request)
        self.service.ping_worker(worker_id, self.request.timestamp)
        return InitResponse(worker_id)


class ProcessorsFactory(object):
    resource_to_processor_map = {
        PingRequest: PingProcessor,
        InitRequest: InitProcessor,
    }

    def __call__(self, service, request):
        factory = self.resource_to_processor_map[type(request)]
        return factory(service, request)
