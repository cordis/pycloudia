from zope.interface import implementer

from pycloudia.activities.clients.consts import HEADER
from pycloudia.activities.facades.interfaces import IClientDirector


@implementer(IClientDirector)
class Director(object):
    logger = None
    encoder = None
    decoder = None

    def __init__(self, facade_id, clients):
        """
        :type facade_id: C{str}
        :type clients: L{pycloudia.activities.clients.interfaces.IService}
        """
        self.facade_id = facade_id
        self.clients_service = clients
        self.clients_map = {}

    def connection_made(self, client):
        self.clients_map[client.client_id] = client
        self.clients_service.create_activity(client.client_id, self.facade_id)

    def connection_lost(self, client, reason):
        try:
            del self.clients_map[client.client_id]
        except KeyError:
            self.logger.log_client_not_found(client.client_id)
        else:
            self.clients_service.delete_activity(client.client_id, reason)

    def connection_done(self, client):
        del self.clients_map[client.client_id]
        self.clients_service.delete_activity(client.client_id)

    def read_message(self, client, message):
        package = self.decoder.decode(message)
        package.headers[HEADER.CLIENT_ID] = client.client_id
        self.clients_service.process_incoming_package(client.client_id, package)

    def send_package(self, package):
        try:
            client_id = package.headers.pop(HEADER.CLIENT_ID)
        except KeyError:
            self.logger.log_header_not_found(HEADER.CLIENT_ID)
        else:
            self._send_package_to_client(package, client_id)

    def _send_package_to_client(self, package, client_id):
        try:
            client = self.clients_map[client_id]
        except KeyError:
            self.logger.log_client_not_found(client_id)
        else:
            message = self.encoder.encode(package)
            client.send_message(message)
