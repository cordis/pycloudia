from pycloudia.defer import deferrable


class BaseChannel(object):
    package_factory = None
    package_decoder = None
    package_encoder = None

    def __init__(self, name, router):
        self.name = name
        self.router = router


class PullChannel(BaseChannel):
    socket = None

    def listen(self, callback):
        @deferrable
        def on_message_received(message):
            package = self.package_decoder.decode(message, self.package_factory)
            return callback(package)
        self.socket.listen(on_message_received)


class PushChannel(BaseChannel):
    sockets = []

    @deferrable
    def request(self, package):
        socket = self.router.choose(self.sockets, package)
        message = self.package_encoder.encode(package)
        return socket.request(message)

    def broadcast(self, package):
        message = self.package_encoder.encode(package)
        for socket in self.sockets:
            socket.push(message)
