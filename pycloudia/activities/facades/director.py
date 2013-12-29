from zope.interface import implementer

from pycloudia.activities.clients.consts import HEADER
from pycloudia.activities.facades.interfaces import IClientDirector


@implementer(IClientDirector)
class Director(object):
    logger = None
    encoder = None
    decoder = None

    def __init__(self, facade_id, service):
        self.facade_id = facade_id
        self.service = service
        self.clients = {}

    def connection_made(self, client):
        self.clients[client.client_id] = client
        self.service.create_activity(client.client_id, self.facade_id)

    def connection_lost(self, client, reason):
        del self.clients[client.client_id]
        self.service.delete_activity(client.client_id, reason)

    def connection_done(self, client):
        del self.clients[client.client_id]
        self.service.delete_activity(client.client_id)

    def read_message(self, client, message):
        package = self.decoder.decode(message)
        package.headers[HEADER.CLIENT_ID] = client.client_id
        self.service.process_incoming_package(client.client_id, package)

    def send_package(self, package):
        try:
            client_id = package.headers.pop(HEADER.CLIENT_ID)
        except KeyError:
            self.logger.warn('Header `%s` not found', HEADER.CLIENT_ID)
        else:
            self._send_package_to_client(package, client_id)

    def _send_package_to_client(self, package, client_id):
        try:
            client = self.clients[client_id]
        except KeyError:
            self.logger.warn('Client `%s` not found', client_id)
        else:
            message = self.encoder.encode(package)
            client.send_message(message)
