from txzmq.connection import ZmqConnection
from zmq.core import constants as zmq_constants


__all__ = [
    'DealerSocketConnection',
    'RouterSocketConnection',
    'PushSocketConnection',
    'PullSocketConnection',
    'PubSocketConnection',
    'SubSocketConnection',
]


class BaseSocketConnection(ZmqConnection):
    def __init__(self, callback, *args, **kwargs):
        self.process_message = staticmethod(callback)
        super(BaseSocketConnection, self).__init__(*args, **kwargs)

    def messageReceived(self, message_parts):
        assert len(message_parts) == 1
        self.process_message(message_parts[0])


class DealerSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.DEALER

    def forward(self, message, identities=None):
        identities = identities or []
        self.send(identities + [message])


class RouterSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.ROUTER

    def messageReceived(self, message_parts):
        assert len(message_parts) > 1
        message = message_parts.pop()
        self.process_message(message, identities=message_parts)


class PushSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.PUSH


class PullSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.PULL


class PubSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.PUB


class SubSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.SUB
