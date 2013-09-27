from pycloudia.defer import inline_callbacks, return_value, deferrable
from pycloudia.channels.declarative import router, dealer
from pycloudia.channels.consts import IMPL
from pycloudia.services.config.consts import CHANNEL


class Service(object):
    reactor = None
    state_factory = None
    request_factory = None
    processor_factory = None

    workers = router(CHANNEL.WORKERS)
    replicas = dealer(CHANNEL.REPLICAS)
    managers = router(CHANNEL.MANAGERS, impl=IMPL.HTTP)

    @deferrable
    def initialize(self):
        self.state = self.state_factory()

    @workers.listen
    @inline_callbacks
    def process_worker_request(self, package, client_id):
        request = self.request_factory(package)
        processor = self.processor_factory(self, request)
        worker_id = self.state.get_or_create_worker_id(client_id)
        response = yield self.reactor.call_entirely(processor.process, worker_id)
        return_value(response)

    @workers.route
    def send_worker_message(self, package, worker_id):
        pass

    @replicas.broadcast
    def send_replica_message(self, package):
        pass

    @managers.listen
    @inline_callbacks
    def process_manage_request(self, package):
        # @TODO: authentication
        pass
