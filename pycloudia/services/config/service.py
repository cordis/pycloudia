from pycloudia.defer import inline_callbacks, return_value, deferrable
from pycloudia.channels.declarative import router
from pycloudia.channels.consts import IMPL
from pycloudia.services.config.consts import CHANNEL


class Service(object):
    reactor = None
    state_factory = None
    request_factory = None
    processor_factory = None

    workers = router(CHANNEL.WORKERS)
    manager = router(CHANNEL.MANAGERS, impl=IMPL.HTTP)

    @deferrable
    def initialize(self):
        self.state = self.state_factory()

    @workers.listen
    @inline_callbacks
    def process_worker_request(self, package, worker_id):
        request = self.request_factory(package)
        processor = self.processor_factory(request)
        response = yield self.reactor.call(worker_id, processor.process, request)
        return_value(response)

    @workers.route
    def send_message_to_worker(self, package, worker_id):
        pass

    @manager.listen
    @inline_callbacks
    def process_manage_request(self, package):
        # @TODO: authentication
        pass
