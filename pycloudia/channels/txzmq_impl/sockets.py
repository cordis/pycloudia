from txzmq import ZmqEndpoint, ZmqEndpointType

from pycloudia.channels.txzmq_impl.connections import *


__all__ = [
    'DealerSocket',
    'RouterSocket',
    'PushSocket',
    'SinkSocket',
    'BlowSocket',
    'PullSocket',
    'PubSocket',
    'SubSocket',
]


class BaseSocket(object):
    endpoint_type = NotImplemented
    connection_factory = NotImplemented

    def __init__(self, zmq_factory, address, identity=None):
        self.factory = zmq_factory
        self.endpoint = ZmqEndpoint(self.endpoint_type, address),
        self.identity = identity
        self.callback = None
        self.connection = None

    def _generate_identity(self):
        return ':'.join(self.endpoint)

    def start(self, callback):
        assert self.connection is None
        self.callback = callback
        self.connection = self._create_connection()

    def _create_connection(self):
        return self.connection_factory(self.callback, self.factory, self.endpoint, self.identity)
    
    def stop(self):
        assert self.connection is not None
        self.connection.shutdown()
        self.connection = None


class DealerSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = DealerSocketConnection

    def start(self, callback):
        assert self.identity is not None
        super(DealerSocket, self).start(callback)


class RouterSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = RouterSocketConnection


class PushSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = PushSocketConnection


class SinkSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PullSocketConnection


class BlowSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PushSocketConnection


class PullSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = PullSocketConnection


class PubSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PubSocketConnection


class SubSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = SubSocketConnection
