from socket import error as CannotListenError

from pycloudia.activities.facades.interfaces import IListener
from pycloudia.activities.facades.exceptions import ListenFailedError


class HttpListener(IListener):
    """
    :type logger: L{ILogger}
    :type io_loop: L{tornado.ioloop.IOLoop}
    :type protocol_factory: L{pycloudia.activities.facades.tornado_impl.protocol.ProtocolFactory}
    """
    logger = None
    io_loop = None
    protocol_factory = None

    def __init__(self, host, min_port=8081, max_port=8084):
        self.host = host
        self.port = None
        self.min_port = min_port
        self.max_port = max_port

    def start(self, director):
        protocol = self.protocol_factory(director)
        for port in range(self.min_port, self.max_port + 1):
            try:
                protocol.listen(port, self.host, io_loop=self.io_loop)
                self.logger.info('Listening started on %s:%s', self.host, port)
            except CannotListenError as e:
                self.logger.info('Listening failed on %s:%s -- %s', self.host, port, e)
            else:
                self.port = port
        raise ListenFailedError(self.host, (self.max_port, self.max_port))
