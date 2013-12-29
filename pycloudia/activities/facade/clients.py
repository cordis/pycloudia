from zope.interface import implementer

from pycloudia.activities.facade.interfaces import IClient, IClientDirector


@implementer(IClient)
class Client(object):
    heartbeat_factory = None

    def __init__(self, director, protocol, client_id=None):
        self.director = director
        self.protocol = protocol
        self.client_id = client_id
        self.heartbeat = self.heartbeat_factory(self)

    def connection_made(self):
        """
        Protocol callback
        """
        self.director.attach_client(self)
        self.heartbeat.start()

    def connection_lost(self):
        """
        Protocol callback
        """
        self.director.send_connection_lost(self)
        self.director.detach_client(self)
        self.heartbeat.stop()

    def string_received(self, message):
        """
        Protocol callback
        """
        self.director.process_incoming_message(self, message)

    def disconnect(self):
        self.protocol.lose_connection()

    def process_outgoing_message(self, message):
        self.heartbeat.reset()
        self.protocol.send_message(message)


@implementer(IClientDirector)
class ClientDirector(object):
    logger = None
    client_factory = Client
    client_id_factory = None

    def __init__(self, identity):
        self.identity = identity
        self.client_map = {}

    def create_client(self, protocol):
        return self.client_factory(self, protocol, self.client_id_factory())

    def attach_client(self, client):
        self.client_map[client.client_id] = client

    def detach_client(self, client):
        try:
            del self.client_map[client.client_id]
        except KeyError:
            pass

    def disconnect_client(self, package):
        pass

    def send_connection_lost(self, client):
        pass

    def process_incoming_message(self, client):
        pass

    def process_outgoing_message(self, message):
        pass

    def _log_client_count(self):
        self.logger.info('Active clients: %d', len(self.client_map))
