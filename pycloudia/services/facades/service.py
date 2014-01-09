from pycloudia.uitls.abstracts import BiDirectedDict
from pycloudia.uitls.defer import deferrable
from pycloudia.services.facades.interfaces import IService, IDirector


class Service(IService, IDirector):
    """
    :type logger: L{pycloudia.services.facades.logger.Logger}
    :type listener: L{pycloudia.services.facades.interfaces.IListener}
    :type encoder: L{pycloudia.packages.interfaces.IEncoder}
    :type decoder: L{pycloudia.packages.interfaces.IDecoder}
    :type clients: L{pycloudia.services.clients.interfaces.IService}
    :type client_id_factory: C{Callable}
    """
    logger = None
    listener = None
    encoder = None
    decoder = None
    clients = None
    client_id_factory = None

    def __init__(self, facade_id):
        """
        :type facade_id: C{str}

        """
        self.facade_id = facade_id
        self.clients_map = BiDirectedDict()

    @deferrable
    def start(self):
        self.listener.start(self)

    def connection_made(self, client):
        self.clients_map[client] = client_id = self.client_id_factory()
        self.clients.create_activity(client_id, self.facade_id)

    def connection_done(self, client):
        self.connection_lost(client, None)

    def connection_lost(self, client, reason):
        try:
            client_id = self.clients_map.pop(client)
        except KeyError:
            self.logger.log_client_not_found(client)
        else:
            self.clients.delete_activity(client_id, reason)

    def read_message(self, client, message):
        try:
            client_id = self.clients_map[client]
        except KeyError:
            self.logger.log_client_not_found(client)
        else:
            package = self.decoder.decode(message)
            self.clients.process_incoming_package(client_id, package)

    def process_outgoing_package(self, facade_id, client_id, package):
        assert facade_id == self.facade_id
        try:
            client = self.clients_map.behind[client_id]
        except KeyError:
            self.logger.log_client_not_found(client_id)
        else:
            message = self.encoder.encode(package)
            client.send_message(message)
