from zmq.eventloop.zmqstream import ZMQStream as ZmqStream
from zmq.sugar import Socket as ZmqSocket
from zmq.core import constants as zmq_constants

from pysigslot import Signal
from pycloudia.zmq_impl.strategies import *


__all__ = [
    'RouterSocket',
    'DealerSocket',
    'SinkSocket',
    'PushSocket',
    'PullSocket',
    'BlowSocket',
    'SubSocket',
    'PubSocket',
]


class BaseSocket(object):
    zmq_socket_factory = ZmqSocket
    zmq_stream_factory = ZmqStream
    zmq_socket_type = NotImplemented
    zmq_stream_start_strategy = NotImplemented
    zmq_stream_message_strategy = NotImplemented

    @classmethod
    def create_instance(cls, zmq_context, io_loop, *args, **kwargs):
        return cls(zmq_context, io_loop, *args, **kwargs)

    def __init__(self, zmq_context, io_loop):
        self.message_received = Signal()
        self.zmq_stream = self._create_zmq_stream(zmq_context, io_loop)

    def _create_zmq_stream(self, zmq_context, io_loop):
        zmq_socket = self.zmq_socket_factory(zmq_context, self.zmq_socket_type)
        zmq_stream = self.zmq_stream_factory(zmq_socket, io_loop)
        return zmq_stream

    def start(self, host, port):
        self.zmq_stream.on_recv(self.on_message_received)
        self.zmq_stream_start_strategy.start(self, host, port)

    def start_on_random_port(self, host, min_port=49152, max_port=65536, max_tries=100):
        self.zmq_stream.on_recv(self.on_message_received)
        return self.zmq_stream_start_strategy.start_on_random_port(host, min_port, max_port, max_tries)

    def on_message_received(self, message_list):
        self.zmq_stream_message_strategy.on_message_received(self, message_list)

    def send(self, message):
        self.zmq_stream_message_strategy.send(self, message)

    def close(self):
        self.zmq_stream.close()
        self.zmq_stream = None
        self.message_received.disconnect_all()

    def __getattr__(self, item):
        if not hasattr(self.zmq_stream, item):
            raise AttributeError('"{0}" object has no attribute "{1}"'.format(type(self), item))
        return getattr(self.zmq_stream, item)

    def __setattr__(self, key, value):
        if not hasattr(self.zmq_stream, key):
            raise AttributeError('"{0}" object has no attribute "{1}"'.format(type(self), key))
        return setattr(self.zmq_stream, key, value)


class RouterSocket(BaseSocket):
    zmq_socket_type = zmq_constants.ROUTER
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_message_strategy = RouterMessageStrategy()


class DealerSocket(BaseSocket):
    zmq_socket_type = zmq_constants.DEALER
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_message_strategy = DealerMessageStrategy()

    def __init__(self, zmq_context, io_loop, identity):
        assert identity is not None
        super(DealerSocket, self).__init__(zmq_context, io_loop)
        self.zmq_stream.socket.identity = identity


class SinkSocket(BaseSocket):
    zmq_socket_type = zmq_constants.PULL
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_message_strategy = SimpleMessageStrategy()


class PushSocket(BaseSocket):
    zmq_socket_type = zmq_constants.PUSH
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_message_strategy = SimpleMessageStrategy()


class PullSocket(BaseSocket):
    zmq_socket_type = zmq_constants.PULL
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_message_strategy = SimpleMessageStrategy()


class BlowSocket(BaseSocket):
    zmq_socket_type = zmq_constants.PUSH
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_message_strategy = SimpleMessageStrategy()


class SubSocket(BaseSocket):
    zmq_socket_type = zmq_constants.SUB
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_message_strategy = SimpleMessageStrategy()


class PubSocket(BaseSocket):
    zmq_socket_type = zmq_constants.PUB
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_message_strategy = SimpleMessageStrategy()
