from pycloudia.uitls.defer import maybe_deferred
from pycloudia.activities.clients.consts import HEADER


class Activity(object):
    router = None
    facade = None

    def __init__(self, facade_id, client_id):
        self.facade_id = facade_id
        self.client_id = client_id

    @maybe_deferred
    def process_incoming_package(self, package):
        package.set_header(HEADER.FACADE_ID, self.facade_id)
        package.set_header(HEADER.CLIENT_ID, self.client_id)
        return self.router.route_package(package)

    @maybe_deferred
    def process_outgoing_package(self, package):
        return self.facade.get_instance(self.facade_id).process_ougoing_package(self.client_id, package)
