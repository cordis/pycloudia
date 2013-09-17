from zmq.core import constants as zmq_constants
from txzmq import ZmqEndpoint, ZmqConnection, ZmqEndpointType


class BaseSocketConnection(ZmqConnection):
    def __init__(self, callback, *args, **kwargs):
        self.process_message = staticmethod(callback)
        super(BaseSocketConnection, self).__init__(*args, **kwargs)

    def messageReceived(self, message):
        self.process_message(message)


class RouterSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.ROUTER


class DealerSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.DEALER


class BaseSocket(object):
    endpoint_type = NotImplemented
    connection_factory = NotImplemented

    def __init__(self, zmq_factory, address, identity=None):
        self.zmq_factory = zmq_factory
        self.address = address
        self.identity = identity
        self.connection = None

    def run(self, on_message_received):
        self.connection = self._create_connection(on_message_received)

    def _create_connection(self, on_message_received):
        endpoint = ZmqEndpoint(self.endpoint_type, self.address)
        return self.connection_factory(on_message_received, self.zmq_factory, endpoint, self.identity)


class RouterSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = RouterSocketConnection


class DealerSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = DealerSocketConnection


class SocketPool(object):
    sockets = []

    def add(self, socket):
        self.sockets.append(socket)

    def run(self, on_message_received):
        for socket in self.sockets:
            socket.run(on_message_received)
