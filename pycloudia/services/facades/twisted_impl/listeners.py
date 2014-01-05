from twisted.internet.interfaces import IReactorTCP
from twisted.internet.error import CannotListenError

from pycloudia.services.facades.interfaces import IListener
from pycloudia.services.facades.exceptions import ListenFailedError


class TcpListener(object, IListener):
    logger = None
    reactor = IReactorTCP

    def __init__(self, protocol_factory, host, min_port=8091, max_port=8094):
        self.protocol_factory = protocol_factory
        self.host = host
        self.port = None
        self.min_port = min_port
        self.max_port = max_port

    def start(self):
        for port in range(self.min_port, self.max_port + 1):
            try:
                self.reactor.listenTCP(port, interface=self.host)
                self.logger.info('Listening started on %s:%s', self.host, port)
            except CannotListenError as e:
                self.logger.info('Listening failed on %s:%s -- %s', self.host, port, e.socketError)
            else:
                self.port = port
        raise ListenFailedError(self.host, (self.max_port, self.max_port))
