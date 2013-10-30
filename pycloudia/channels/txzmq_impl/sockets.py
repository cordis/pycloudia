from txzmq import ZmqEndpoint, ZmqEndpointType

from pycloudia.channels.txzmq_impl.connections import *
from pycloudia.channels.txzmq_impl.strategies import *


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
    message_strategy_factory = NotImplemented

    def __init__(self, zmq_factory, address, identity=None):
        self.factory = zmq_factory
        self.endpoint = ZmqEndpoint(self.endpoint_type, address),
        self.identity = identity
        self.callback = None
        self.connection = None
        self.message_strategy = self.message_strategy_factory(self)

    def _generate_identity(self):
        return ':'.join(self.endpoint)

    def start(self, callback):
        assert self.connection is None
        self.callback = callback
        self.connection = self._create_connection()

    def _create_connection(self):
        return self.connection_factory(self._on_message_received, self.factory, self.endpoint, self.identity)

    def _on_message_received(self, message_list):
        self.message_strategy.on_message_received(message_list)

    def send(self, message):
        self.message_strategy.send_message(message)

    def stop(self):
        assert self.connection is not None
        self.connection.shutdown()
        self.connection = None


class DealerSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = DealerSocketConnection
    message_strategy_factory = DealerMessageStrategy

    def start(self, callback):
        assert self.identity is not None
        super(DealerSocket, self).start(callback)


class RouterSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = RouterSocketConnection
    message_strategy_factory = RouterMessageStrategy


class PushSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = PushSocketConnection
    message_strategy_factory = SimpleMessageStrategy


class SinkSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PullSocketConnection
    message_strategy_factory = SimpleMessageStrategy


class BlowSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PushSocketConnection
    message_strategy_factory = SimpleMessageStrategy


class PullSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = PullSocketConnection
    message_strategy_factory = SimpleMessageStrategy


class PubSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PubSocketConnection
    message_strategy_factory = SimpleMessageStrategy


class SubSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = SubSocketConnection
    message_strategy_factory = SimpleMessageStrategy
