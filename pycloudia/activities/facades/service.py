from pycloudia.utils.structs import BiDirectedDict
from pycloudia.utils.defer import deferrable, inline_callbacks

from pycloudia.activities.facades.exceptions import ClientNotFoundError
from pycloudia.activities.facades.interfaces import IService, IDirector


class Service(IService, IDirector):
    """
    :type logger: L{pycloudia.activities.facades.logger.Logger}
    :type reactor: C{pycloudia.reactor.interfaces.IIsolatedReactor}
    :type encoder: L{pycloudia.packages.interfaces.IEncoder}
    :type decoder: L{pycloudia.packages.interfaces.IDecoder}
    :type listener: L{pycloudia.activities.facades.interfaces.IListener}
    :type sessions: L{pycloudia.activities.facades.interfaces.ISessionRegistry}
    """
    logger = None
    reactor = None
    encoder = None
    decoder = None
    listener = None
    sessions = None

    def __init__(self):
        self.session_map = BiDirectedDict()

    @deferrable
    def start(self):
        self.listener.start(self)

    @inline_callbacks
    def connection_made(self, client):
        self.session_map[client] = yield self.sessions.create()

    def connection_done(self, client):
        self.connection_lost(client, None)

    @inline_callbacks
    def connection_lost(self, client, reason):
        try:
            session = self.session_map.pop(client)
        except KeyError:
            self.logger.log_client_not_found(client)
        else:
            yield self.sessions.delete(session, reason)

    @inline_callbacks
    def read_message(self, client, message):
        package = self.decoder.decode(message)
        yield self.read_package(package)

    @inline_callbacks
    def read_package(self, client, package):
        try:
            session = self.session_map[client]
        except KeyError:
            self.logger.log_client_not_found(client)
        else:
            yield session.process_incoming_package(package)

    def process_outgoing_package(self, session, package):
        client = self._get_client_by_session(session)
        message = self.encoder.encode(package)
        client.send_message(message)

    def _get_client_by_session(self, session):
        """
        :type session: L{pycloudia.activities.facades.interfaces.ISession}
        :rtype: L{pycloudia.activities.facades.interfaces.IClient}
        :raise: L{pycloudia.activities.facades.exceptions.ClientNotFoundError}
        """
        try:
            return self.session_map.behind[session]
        except KeyError:
            raise ClientNotFoundError(session)
