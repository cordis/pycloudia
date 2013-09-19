from txzmq import ZmqEndpoint, ZmqEndpointType

from pycloudia.channels.twisted_zmq.connections import *


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
    identity = None
    endpoint_type = NotImplemented
    connection_factory = NotImplemented

    def __init__(self, zmq_factory, address):
        self.factory = zmq_factory
        self.endpoint = ZmqEndpoint(self.endpoint_type, address),
        self.connection = None

    def run(self, on_message_received):
        assert self.connection is None
        self.connection = self._create_connection(on_message_received)

    def _create_connection(self, on_message_received):
        return self.connection_factory(
            on_message_received,
            self.factory,
            self.endpoint,
            self.identity
        )


class DealerSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = DealerSocketConnection


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
