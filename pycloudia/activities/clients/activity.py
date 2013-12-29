from pycloudia.uitls.defer import maybe_deferred
from pycloudia.activities.clients.consts import HEADER


class Activity(object):
    logger = None
    router = None
    facade = None

    def __init__(self, client_id, facade_id):
        self.client_id = client_id
        self.facade_id = facade_id

    @maybe_deferred
    def process_incoming_package(self, package):
        package.headers[HEADER.CLIENT_ID] = self.client_id
        package.headers[HEADER.FACADE_ID] = self.facade_id
        return self.router.route_package(package)

    @maybe_deferred
    def process_outgoing_package(self, package):
        try:
            facade = self.facade.get_activity(self.facade_id)
        except KeyError:
            self.logger.warn('Facade `%s` not found', self.facade_id)
        else:
            return facade.process_ougoing_package(self.client_id, package)
