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
        self.callback = staticmethod(callback)
        super(BaseSocketConnection, self).__init__(*args, **kwargs)

    def messageReceived(self, message_part_list):
        self.callback(message_part_list)


class DealerSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.DEALER


class RouterSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.ROUTER


class PushSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.PUSH


class PullSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.PULL


class PubSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.PUB


class SubSocketConnection(BaseSocketConnection):
    socketType = zmq_constants.SUB
