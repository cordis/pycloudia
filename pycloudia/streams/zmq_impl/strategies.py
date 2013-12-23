from pycloudia.streams.zmq_impl.messages import Message


__all__ = [
    'BindStartStrategy',
    'ConnectStartStrategy',
    'SimpleReadMessageStrategy',
    'SignedReadMessageStrategy',
    'DealerReadMessageStrategy',
    'SimpleSendMessageStrategy',
    'SignedSendMessageStrategy',
    'DealerSendMessageStrategy',
]


class BaseStartStrategy(object):
    ADDRESS_TCP_HOST = 'tcp://{0}'
    ADDRESS_TCP_HOST_PORT = 'tcp://{0}:{1}'

    def start_tcp(self, stream, host, port):
        raise NotImplementedError()

    def start_tcp_on_random_port(self, stream, host, *args, **kwargs):
        raise NotImplementedError()

    def _create_tcp_host_address(self, host):
        return self.ADDRESS_TCP_HOST.format(host)

    def _create_tcp_host_port_address(self, host, port):
        return self.ADDRESS_TCP_HOST_PORT.format(host, port)


class ConnectStartStrategy(BaseStartStrategy):
    def start_tcp(self, stream, host, port):
        address = self._create_tcp_host_port_address(host, port)
        stream.connect(address)


class BindStartStrategy(BaseStartStrategy):
    def start_tcp(self, stream, host, port):
        address = self._create_tcp_host_port_address(host, port)
        stream.bind(address)

    def start_tcp_on_random_port(self, stream, host, *args, **kwargs):
        address = self._create_tcp_host_address(host)
        return stream.bind_to_random_port(address, *args, **kwargs)


class BaseReadMessageStrategy(object):
    message_factory = Message

    def on_message_received(self, stream, message_list):
        raise NotImplementedError()


class SimpleReadMessageStrategy(BaseReadMessageStrategy):
    def on_message_received(self, stream, message_list):
        assert len(message_list) == 1
        message = self.message_factory(message_list[0])
        stream.message_received.emit(message)


class SignedReadMessageStrategy(BaseReadMessageStrategy):
    def on_message_received(self, stream, message_list):
        assert len(message_list) > 1
        message = self.message_factory(message_list[-1], peer=message_list[0], hops=message_list[1:-1])
        stream.message_received.emit(message)


class DealerReadMessageStrategy(BaseReadMessageStrategy):
    def on_message_received(self, stream, message_list):
        assert len(message_list) > 0
        message = self.message_factory(message_list[-1], peer=stream.zmq_stream.socket.identity, hops=message_list[:-1])
        stream.message_received.emit(message)


class BaseSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        raise NotImplementedError()


class SimpleSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        stream.zmq_stream.send(message)


class SignedSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        stream.zmq_stream.send_multipart([message.peer] + message.hops + [message])


class DealerSendMessageStrategy(object):
    @staticmethod
    def send_message(stream, message):
        stream.zmq_stream.send_multipart(message.hops + [message])
