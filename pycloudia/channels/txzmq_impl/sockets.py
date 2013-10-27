from txzmq import ZmqEndpoint, ZmqEndpointType

from pycloudia.channels.txzmq_impl.connections import *


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

    def __init__(self, zmq_factory, address, guid=None):
        self.factory = zmq_factory
        self.endpoint = ZmqEndpoint(self.endpoint_type, address),
        self.guid = guid or self._generate_guid()
        self.callback = None
        self.connection = None

    def _generate_guid(self):
        return ':'.join(self.endpoint)

    def start(self, callback):
        assert self.connection is None
        self.callback = callback
        self.connection = self._create_connection()

    def _create_connection(self):
        return self.connection_factory(
            self._on_message_received,
            self.factory,
            self.endpoint,
            self.guid
        )
    
    def _on_message_received(self, message_list):
        raise NotImplementedError()

    def stop(self):
        assert self.connection is not None
        self.connection.shutdown()
        self.connection = None


class DealerSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = DealerSocketConnection

    def _on_message_received(self, message_list):
        return self.callback(message_list[0], self.guid)


class RouterSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = RouterSocketConnection

    def _on_message_received(self, message, identities=None):

        class MessageWrapper(type(message)):
            identities = identities

        return self.callback(MessageWrapper(message))


class PushSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = PushSocketConnection


class SinkSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PullSocketConnection

    def _on_message_received(self, message_list):
        self.callback(message_list[0], None)
        return None


class BlowSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PushSocketConnection


class PullSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = PullSocketConnection

    def _on_message_received(self, message_list):
        self.callback(message_list[0], self.guid)
        return None


class PubSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.bind
    connection_factory = PubSocketConnection


class SubSocket(BaseSocket):
    endpoint_type = ZmqEndpointType.connect
    connection_factory = SubSocketConnection

    def _on_message_received(self, message_list):
        self.callback(message_list[0], self.guid)
        return None
