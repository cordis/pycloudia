from zope.interface import implementer

from pycloudia.streams.zmq_impl.messages import Message
from pycloudia.streams.zmq_impl.interfaces import *


__all__ = [
    'BindStartStrategy',
    'ConnectStartStrategy',
    'RejectReadMessageStrategy',
    'SimpleReadMessageStrategy',
    'SignedReadMessageStrategy',
    'DealerReadMessageStrategy',
    'RejectSendMessageStrategy',
    'SimpleSendMessageStrategy',
    'SignedSendMessageStrategy',
    'DealerSendMessageStrategy',
    'RouterSendMessageStrategy',
]


class BaseStartStrategy(object):
    ADDRESS_TCP_HOST = 'tcp://{0}'
    ADDRESS_TCP_HOST_PORT = 'tcp://{0}:{1}'

    def _create_tcp_host_address(self, host):
        return self.ADDRESS_TCP_HOST.format(host)

    def _create_tcp_host_port_address(self, host, port):
        return self.ADDRESS_TCP_HOST_PORT.format(host, port)


@implementer(IStartStreamStrategy)
class ConnectStartStrategy(BaseStartStrategy):
    def start_tcp(self, stream, host, port):
        address = self._create_tcp_host_port_address(host, port)
        stream.connect(address)

    def start_tcp_on_random_port(self, stream, host, *args, **kwargs):
        raise NotImplementedError('Unable to connect to random tcp port')


@implementer(IStartStreamStrategy)
class BindStartStrategy(BaseStartStrategy):
    def start_tcp(self, stream, host, port):
        address = self._create_tcp_host_port_address(host, port)
        stream.bind(address)

    def start_tcp_on_random_port(self, stream, host, *args, **kwargs):
        address = self._create_tcp_host_address(host)
        return stream.bind_to_random_port(address, *args, **kwargs)


@implementer(IReadStreamMessageStrategy)
class RejectReadMessageStrategy(object):
    def message_factory(self):
        raise NotImplementedError('Unable to provide message factory for write-only stream')

    def read_message(self, stream, message_list):
        raise NotImplementedError('Unable to read write-only stream message')


@implementer(IReadStreamMessageStrategy)
class SimpleReadMessageStrategy(object):
    message_factory = Message

    def read_message(self, stream, message_list):
        assert len(message_list) == 1
        message = self.message_factory(message_list[0])
        stream.message_received.emit(message)


@implementer(IReadStreamMessageStrategy)
class SignedReadMessageStrategy(object):
    message_factory = Message

    def read_message(self, stream, message_list):
        assert len(message_list) > 1
        message = self.message_factory(message_list[-1], peer=message_list[0], hops=message_list[1:-1])
        stream.message_received.emit(message)


@implementer(IReadStreamMessageStrategy)
class DealerReadMessageStrategy(object):
    message_factory = Message

    def read_message(self, stream, message_list):
        assert len(message_list) > 0
        message = self.message_factory(message_list[-1], peer=stream.identity, hops=message_list[:-1])
        stream.message_received.emit(message)


@implementer(ISendStreamMessageStrategy)
class RejectSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        raise NotImplementedError('Unable to send message to read-only stream')


@implementer(ISendStreamMessageStrategy)
class SimpleSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        stream.zmq_stream.send_message(message)


@implementer(ISendStreamMessageStrategy)
class DealerSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        stream.zmq_stream.send_multipart(message.hops + [message])


@implementer(ISendStreamMessageStrategy)
class SignedSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        stream.zmq_stream.send_multipart([stream.identity] + message.hops + [message])


@implementer(ISendStreamMessageStrategy)
class RouterSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        stream.zmq_stream.send_multipart([message.peer] + message.hops + [message])
