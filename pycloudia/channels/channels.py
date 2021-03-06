from collections import deque

from pycloudia.consts import PACKAGE
from pycloudia.utils.defer import inline_callbacks, maybe_deferred, Deferred
from pycloudia.channels.messages import ChannelMessage
from pycloudia.cluster.respondent import ResponderNotFoundError


class RouterPeers(object):
    def __init__(self):
        self.socket = None
        self.callback_list = deque()

    def set_socket(self, socket):
        self.socket = socket
        self.socket.start(self._on_message_received)

    def add_callback(self, callback):
        self.callback_list.append(callback)

    def send(self, message):
        self.socket.send_message(message)

    @inline_callbacks
    def _on_message_received(self, message):
        for callback in self.callback_list:
            yield callback(message)


class DealerPeers(object):
    def __init__(self):
        self.sockets_map = {}
        self.callback_list = deque()

    def add_socket(self, socket):
        self.sockets_map[socket.identity] = socket
        socket.start(self._on_message_received)

    def add_callback(self, callback):
        self.callback_list.append(callback)

    def send(self, message):
        self.sockets_map[message.peer].send_message(message)

    @inline_callbacks
    def _on_message_received(self, message):
        for callback in self.callback_list:
            yield callback(message)


class BiDirectionalChannel(object):
    package_decoder = None
    package_encoder = None
    respondent = None

    message_factory = ChannelMessage
    respondent_header_list = [
        PACKAGE.HEADER.PEER,
        PACKAGE.HEADER.HOPS,
        PACKAGE.HEADER.REQUEST_ID,
    ]

    def __init__(self, callback, peers):
        self.callback = callback
        self.peers = peers
        self.peers.add_callback(self._on_message_received)

    def send_request(self, package):
        deferred = self._register_request(package)
        self.send_package(package)
        return deferred

    def _register_request(self, package):
        request_id = package.get_headers()[PACKAGE.HEADER.REQUEST_ID]
        return self.respondent.listen(request_id, Deferred())

    def _on_message_received(self, message):
        incoming_package = self._decode_package(message)
        try:
            self._process_response(incoming_package)
        except (KeyError, ResponderNotFoundError):
            self._process_request(incoming_package)

    def _decode_package(self, message):
        package = self.package_decoder.decode(message)
        package.get_headers()[PACKAGE.HEADER.PEER] = message.peer
        package.get_headers()[PACKAGE.HEADER.HOPS] = message.hops
        return package

    def _process_response(self, incoming_package):
        request_id = incoming_package.get_headers()[PACKAGE.HEADER.REQUEST_ID]
        self.respondent.resolve(request_id, incoming_package)

    @inline_callbacks
    def _process_request(self, incoming_package):
        outgoing_package = yield maybe_deferred(self.callback, incoming_package)
        if outgoing_package is not None:
            outgoing_package = self._copy_headers_from_request_to_response(incoming_package, outgoing_package)
            self.send_package(outgoing_package)

    def _copy_headers_from_request_to_response(self, incoming_package, outgoing_package):
        for header_name in self.respondent_header_list:
            outgoing_package.get_headers()[header_name] = incoming_package.get_headers()[header_name]
        return outgoing_package

    def send_package(self, package):
        message = self._encode_package(package)
        self.peers.send_message(message)

    def _encode_package(self, package):
        return self.message_factory(
            self.package_encoder.encode(package),
            package.get_headers()[PACKAGE.HEADER.PEER],
            package.get_headers()[PACKAGE.HEADER.HOPS]
        )
