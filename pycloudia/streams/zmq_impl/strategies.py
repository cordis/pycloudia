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


class ConnectStartStrategy(BaseStartStrategy, IStartStreamStrategy):
    def start_tcp(self, stream, host, port):
        address = self._create_tcp_host_port_address(host, port)
        stream.connect(address)

    def start_tcp_on_random_port(self, stream, host, *args, **kwargs):
        raise NotImplementedError('Unable to connect to random tcp port')


class BindStartStrategy(BaseStartStrategy, IStartStreamStrategy):
    def start_tcp(self, stream, host, port):
        address = self._create_tcp_host_port_address(host, port)
        stream.bind(address)

    def start_tcp_on_random_port(self, stream, host, *args, **kwargs):
        address = self._create_tcp_host_address(host)
        return stream.bind_to_random_port(address, *args, **kwargs)


class RejectReadMessageStrategy(IReadStreamMessageStrategy):
    def read_message(self, stream, message_list):
        raise NotImplementedError('Unable to read write-only stream message')


class SimpleReadMessageStrategy(IReadStreamMessageStrategy):
    def read_message(self, stream, message_list):
        assert len(message_list) == 1
        message = stream.zmq_message_factory(message_list[0])
        stream.on_read.emit(message)


class SignedReadMessageStrategy(IReadStreamMessageStrategy):
    def read_message(self, stream, message_list):
        assert len(message_list) > 1
        message = stream.zmq_message_factory(message_list[-1], peer=message_list[0], hops=message_list[1:-1])
        stream.on_read.emit(message)


class DealerReadMessageStrategy(IReadStreamMessageStrategy):
    def read_message(self, stream, message_list):
        assert len(message_list) > 0
        message = stream.zmq_message_factory(message_list[-1], peer=stream.identity, hops=message_list[:-1])
        stream.on_read.emit(message)


class RejectSendMessageStrategy(ISendStreamMessageStrategy):
    @staticmethod
    def send_message(self, stream, message):
        raise NotImplementedError('Unable to send message to read-only stream')


class SimpleSendMessageStrategy(ISendStreamMessageStrategy):
    @staticmethod
    def send_message(self, stream, message):
        stream.zmq_stream.send(message)


class DealerSendMessageStrategy(ISendStreamMessageStrategy):
    @staticmethod
    def send_message(self, stream, message):
        stream.zmq_stream.send_multipart(message.hops + [message])


class SignedSendMessageStrategy(ISendStreamMessageStrategy):
    @staticmethod
    def send_message(self, stream, message):
        stream.zmq_stream.send_multipart([stream.identity] + message.hops + [message])


class RouterSendMessageStrategy(ISendStreamMessageStrategy):
    @staticmethod
    def send_message(self, stream, message):
        stream.zmq_stream.send_multipart([message.peer] + message.hops + [message])
