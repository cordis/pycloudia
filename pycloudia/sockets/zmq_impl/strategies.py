from pycloudia.sockets.zmq_impl.messages import Message


__all__ = [
    'BindStartStrategy',
    'ConnectStartStrategy',
    'SimpleMessageStrategy',
    'RouterMessageStrategy',
    'DealerMessageStrategy',
]


class BaseStartStrategy(object):
    ADDRESS_TCP_HOST = 'tcp://{0}'
    ADDRESS_TCP_HOST_PORT = 'tcp://{0}:{1}'

    def start_tcp(self, socket, host, port):
        raise NotImplementedError()

    def start_tcp_on_random_port(self, socket, host, *args, **kwargs):
        raise NotImplementedError()

    def _create_tcp_host_address(self, host):
        return self.ADDRESS_TCP_HOST.format(host)

    def _create_tcp_host_port_address(self, host, port):
        return self.ADDRESS_TCP_HOST_PORT.format(host, port)


class ConnectStartStrategy(BaseStartStrategy):
    def start_tcp(self, socket, host, port):
        address = self._create_tcp_host_port_address(host, port)
        socket.connect(address)


class BindStartStrategy(BaseStartStrategy):
    def start_tcp(self, socket, host, port):
        address = self._create_tcp_host_port_address(host, port)
        socket.bind(address)

    def start_tcp_on_random_port(self, socket, host, *args, **kwargs):
        address = self._create_tcp_host_address(host)
        return socket.bind_to_random_port(address, *args, **kwargs)


class BaseMessageStrategy(object):
    message_factory = Message

    def on_message_received(self, socket, message_list):
        raise NotImplementedError()

    def send_message(self, socket, message):
        raise NotImplementedError()


class SimpleMessageStrategy(BaseMessageStrategy):
    def on_message_received(self, socket, message_list):
        assert len(message_list) == 1
        message = self.message_factory(message_list[0])
        socket.message_received.emit(message)

    def send_message(self, socket, message):
        socket.zmq_stream.send(message)


class RouterMessageStrategy(BaseMessageStrategy):
    def on_message_received(self, socket, message_list):
        assert len(message_list) > 1
        message = self.message_factory(message_list[-1], peer=message_list[0], hops=message_list[1:-1])
        socket.message_received.emit(message)

    def send_message(self, socket, message):
        socket.zmq_stream.send_multipart([message.peer] + message.hops + [message])


class DealerMessageStrategy(BaseMessageStrategy):
    def on_message_received(self, socket, message_list):
        assert len(message_list) > 0
        message = self.message_factory(message_list[-1], peer=socket.zmq_stream.socket.identity, hops=message_list[:-1])
        socket.message_received.emit(message)

    def send_message(self, socket, message):
        socket.zmq_stream.send_multipart(message.hops + [message])
