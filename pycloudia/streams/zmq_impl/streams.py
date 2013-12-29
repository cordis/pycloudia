from zmq.eventloop.zmqstream import ZMQStream as ZmqStream
from zmq.sugar import Socket as ZmqSocket
from zmq.sugar import constants as zmq_constants

from pysigslot import Signal

from pycloudia.streams.zmq_impl.messages import Message
from pycloudia.streams.zmq_impl.strategies import *


__all__ = [
    'RouterStream',
    'DealerStream',
    'SinkStream',
    'PushStream',
    'PullStream',
    'BlowStream',
    'SubStream',
    'PubStream',
]


class BaseStream(object):
    zmq_message_factory = Message
    zmq_socket_factory = ZmqSocket
    zmq_stream_factory = ZmqStream
    zmq_socket_type = NotImplemented
    zmq_stream_start_strategy = NotImplemented
    zmq_stream_read_strategy = NotImplemented
    zmq_stream_send_strategy = NotImplemented

    @classmethod
    def create_instance(cls, zmq_context, zmq_io_loop, *args, **kwargs):
        return cls(zmq_context, zmq_io_loop, *args, **kwargs)

    def __init__(self, zmq_context, zmq_io_loop):
        self.__dict__['zmq_stream'] = self._create_zmq_stream(zmq_context, zmq_io_loop)
        self.__dict__['message_received'] = Signal()

    def _create_zmq_stream(self, zmq_context, zmq_io_loop):
        zmq_socket = self.zmq_socket_factory(zmq_context, self.zmq_socket_type)
        zmq_stream = self.zmq_stream_factory(zmq_socket, zmq_io_loop)
        return zmq_stream

    def start(self, host, port):
        self.zmq_stream.on_recv(self._read_message)
        self.zmq_stream_start_strategy.start_tcp(self, host, port)

    def start_on_random_port(self, host, min_port=49152, max_port=65536, max_tries=100):
        self.zmq_stream.on_recv(self._read_message)
        return self.zmq_stream_start_strategy.start_tcp_on_random_port(
            self.zmq_stream,
            host,
            min_port,
            max_port,
            max_tries
        )

    def _read_message(self, message_list):
        self.zmq_stream_read_strategy.read_message(self, message_list)

    def send_message(self, message):
        self.zmq_stream_send_strategy.send_message(self, message)

    def encode_message_string(self, message_string):
        return self.zmq_message_factory(message_string)

    def close(self):
        self.zmq_stream.close()
        self.zmq_stream = None
        self.message_received.disconnect_all()

    def __getattr__(self, item):
        if not hasattr(self.zmq_stream.socket, item):
            raise AttributeError('"{0}" object has no attribute "{1}"'.format(type(self), item))
        return getattr(self.zmq_stream.socket, item)

    def __setattr__(self, key, value):
        if not hasattr(self.zmq_stream.socket, key):
            raise AttributeError('"{0}" object has no attribute "{1}"'.format(type(self), key))
        return setattr(self.zmq_stream.socket, key, value)


class RouterStream(BaseStream):
    zmq_socket_type = zmq_constants.ROUTER
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_read_strategy = SignedReadMessageStrategy()
    zmq_stream_send_strategy = RouterSendMessageStrategy()


class DealerStream(BaseStream):
    zmq_socket_type = zmq_constants.DEALER
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_read_strategy = DealerReadMessageStrategy()
    zmq_stream_send_strategy = DealerSendMessageStrategy()

    def __init__(self, zmq_context, zmq_io_loop, identity):
        assert identity is not None
        super(DealerStream, self).__init__(zmq_context, zmq_io_loop)
        self.zmq_stream.socket.identity = identity

    @property
    def identity(self):
        return self.zmq_stream.socket.identity


class SinkStream(BaseStream):
    zmq_socket_type = zmq_constants.PULL
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_read_strategy = SignedReadMessageStrategy()
    zmq_stream_send_strategy = RejectSendMessageStrategy()


class PushStream(BaseStream):
    zmq_socket_type = zmq_constants.PUSH
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_read_strategy = RejectReadMessageStrategy()
    zmq_stream_send_strategy = SignedSendMessageStrategy()

    def __init__(self, zmq_context, zmq_io_loop, identity):
        assert identity is not None
        super(PushStream, self).__init__(zmq_context, zmq_io_loop)
        self.identity = identity


class PullStream(BaseStream):
    zmq_socket_type = zmq_constants.PULL
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_read_strategy = SimpleReadMessageStrategy()
    zmq_stream_send_strategy = RejectSendMessageStrategy()


class BlowStream(BaseStream):
    zmq_socket_type = zmq_constants.PUSH
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_read_strategy = RejectReadMessageStrategy()
    zmq_stream_send_strategy = SimpleSendMessageStrategy()


class SubStream(BaseStream):
    zmq_socket_type = zmq_constants.SUB
    zmq_stream_start_strategy = ConnectStartStrategy()
    zmq_stream_read_strategy = SimpleReadMessageStrategy()
    zmq_stream_send_strategy = RejectSendMessageStrategy()


class PubStream(BaseStream):
    zmq_socket_type = zmq_constants.PUB
    zmq_stream_start_strategy = BindStartStrategy()
    zmq_stream_read_strategy = RejectReadMessageStrategy()
    zmq_stream_send_strategy = SimpleSendMessageStrategy()
