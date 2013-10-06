from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.channels.declarative import router, dealer
from pycloudia.services.config.consts import CHANNEL


class ConfigServiceInvoker(object):
    reactor = None
    service_factory = None
    request_factory = None
    processor_factory = None

    consumer = router(CHANNEL.CONFIG)
    replicas = dealer(CHANNEL.CONFIG)

    def __init__(self, runtime):
        self.runtime = runtime

    @deferrable
    def initialize(self):
        self.service = self.service_factory(self.runtime)

    @consumer.consume
    @inline_callbacks
    def process_request(self, package, client_id):
        request = self.request_factory(package)
        processor = self.processor_factory(self.service, request)
        worker_id = self.service.get_or_create_worker_id(client_id)
        response = yield self.reactor.call_entirely(worker_id, processor.process)
        return_value(response)

    @consumer.route
    def send_message_to_worker(self, package, client_id):
        pass

    @replicas.broadcast
    def send_message_to_replica(self, package):
        pass
