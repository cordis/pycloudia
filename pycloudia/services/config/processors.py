from pycloudia.defer import deferrable
from pycloudia.services.config.requests import PingRequest, InitRequest
from pycloudia.services.config.responses import PingResponse, InitResponse


class BaseProcessor(object):
    @deferrable
    def process(self, state, request):
        raise NotImplementedError()


class PingProcessor(BaseProcessor):
    @deferrable
    def process(self, state, request):
        worker_id = state.create_worker_id(request.worker.host, request.worker.port)
        state.update_worker_status(worker_id, request.timestamp)
        return PingResponse()


class InitProcessor(BaseProcessor):
    @deferrable
    def process(self, state, request):
        worker_id = state.create_worker_id(request.worker.host, request.worker.port)
        state.update_worker_state(worker_id, request.timestamp)
        config = state.get_worker_config(worker_id)
        return InitResponse(config)


class ProcessorsFactory(object):
    resource_to_processor_map = {
        PingRequest: PingProcessor(),
        InitRequest: InitProcessor(),
    }

    def __call__(self, request):
        return self.resource_to_processor_map[type(request)]
