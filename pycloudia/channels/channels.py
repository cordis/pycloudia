from zope.interface import implements
from pycloudia.consts import PACKAGE

from pycloudia.uitls.defer import deferrable, inline_callbacks, maybe_deferred, Deferred
from pycloudia.channels.interfaces import *


class BaseChannel(object):
    request_response_registry = None
    package_decoder = None
    package_encoder = None

    def __init__(self, guid, handler):
        self.guid = guid
        self.handler = handler

    def _register_request(self, package):
        deferred = Deferred()
        request_id = self.request_response_registry.set(deferred)
        package.get_headers()[PACKAGE.HEADER.REQUEST_ID] = request_id
        return deferred


class ServerChannel(BaseChannel):
    socket = None

    def set_socket(self, socket):
        if self.socket is not None:
            self.socket.stop()
        self.socket = socket
        self.socket.run(self._on_message_received)

    @inline_callbacks
    def _on_message_received(self, message, client_id):
        incoming_package = self.package_decoder.decode(message)
        response = yield maybe_deferred(self.handler.consume, incoming_package)
        if response is not None:
            self.send_to_client(client_id, response)

    def request_client(self, client_id, package):
        deferred = self._register_request(package)
        self.send_to_client(client_id, package)
        return deferred

    def send_to_client(self, client_id, package):
        message = self.package_encoder.encode(package)
        self.socket.send(client_id, message)


class ClientChannel(BaseChannel):
    sockets = SocketsRegistry()

    def update_sockets(self, socket_list):
        for socket in self.sockets.get_removed(socket_list):
            socket.stop()
        for socket in self.sockets.get_created(socket_list):
            socket.run(self._on_message_received)
        self.sockets = SocketsRegistry(socket_list)

    @inline_callbacks
    def _on_message_received(self, message):
        package = self.package_decoder.decode(message)
        yield maybe_deferred(self.handler.consume, package)

    @deferrable
    def request_socket(self, package, router):
        sender = router.choose(self.sockets, package)
        return sender.send()


class Channel(object):
    implements(ConsumeInterface, ProduceInterface, RouteInterface, BroadcastInterface)







    @deferrable
    def produce(self, package):

        socket = self.socket.get_sender_by_name(sender)
        package = self.package_encoder.encode(package)
        return socket.request(package)

    @deferrable
    def broadcast(self, package):
        sender = self.socket.get_broadcast_sender_name()
        socket = self.socket.get_sender_by_name(sender)
        message = self.package_encoder.encode(package)
        return socket.publish(message)


class SocketsRegistry(object):
    def __init__(self, socket_list=None):
        self.socket_list = socket_list or []
        self.socket_map = dict([(socket.guid, socket) for socket in socket_list])

    def get_removed(self, socket_list):
        return set(self.socket_list) - set(socket_list)

    def get_created(self, socket_list):
        return set(socket_list) - set(self.socket_list)

    def get_by_guid(self, guid):
        return self.socket_map[guid]

    def __iter__(self):
        return iter(self.socket_list)
