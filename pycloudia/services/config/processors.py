from pycloudia.defer import deferrable
from pycloudia.services.config.requests import PingRequest, InitRequest
from pycloudia.services.config.responses import PingResponse, InitResponse


class BaseProcessor(object):
    def __init__(self, state):
        self.state = state

    @deferrable
    def process(self, request):
        raise NotImplementedError()


class PingProcessor(BaseProcessor):
    @deferrable
    def process(self, request):
        worker_id = self.state.create_worker_id(request.worker.host, request.worker.port)
        self.state.update_worker_status(worker_id, request.timestamp)
        return PingResponse()


class InitProcessor(BaseProcessor):
    @deferrable
    def process(self, request):
        worker_id = self.state.create_worker_id(request.worker.host, request.worker.port)
        self.state.update_worker_state(worker_id, request.timestamp)
        config = self.state.get_worker_config(worker_id)
        return InitResponse(config)


class ProcessorsFactory(object):
    def __init__(self, state):
        self.resource_to_processor_map = {
            PingRequest: PingProcessor(state),
            InitRequest: InitProcessor(state),
        }

    def __call__(self, request):
        return self.resource_to_processor_map[type(request)]
