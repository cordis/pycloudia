from pycloudia.channels.messages import ChannelMessage


__all__ = [
    'SimpleMessageStrategy',
    'RouterMessageStrategy',
    'DealerMessageStrategy',
]


class BaseMessageStrategy(object):
    message_factory = ChannelMessage

    def __init__(self, socket):
        self.socket = socket

    def on_message_received(self, message_list):
        raise NotImplementedError()

    def send_message(self, message):
        raise NotImplementedError()


class SimpleMessageStrategy(BaseMessageStrategy):
    def on_message_received(self, message_list):
        assert len(message_list) == 1
        message = self.message_factory(message_list[0])
        self.socket.callback(message)

    def send_message(self, message):
        self.socket.connection.send(message)


class RouterMessageStrategy(BaseMessageStrategy):
    def on_message_received(self, message_list):
        assert len(message_list) > 1
        message = self.message_factory(message_list[-1], peer=message_list[0], hops=message_list[1:-1])
        self.socket.callback(message)

    def send_message(self, message):
        self.socket.connection.send([message.peer] + message.hops + [message])


class DealerMessageStrategy(BaseMessageStrategy):
    def on_message_received(self, message_list):
        assert len(message_list) > 0
        message = self.message_factory(message_list[-1], peer=self.socket.identity, hops=message_list[:-1])
        self.socket.callback(message)

    def send_message(self, message):
        self.socket.connection.send(message.hops + [message])
