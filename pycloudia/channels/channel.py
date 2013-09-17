from pycloudia.defer import deferrable


class BaseChannel(object):
    socket = None
    package_factory = None
    package_decoder = None
    package_encoder = None

    def __init__(self, name, router=None):
        self.name = name
        self.router = router

    def run(self, callback):
        @deferrable
        def on_message_received(message):
            package = self.package_decoder.decode(message, self.package_factory)
            return callback(package)
        self.socket.run(on_message_received)


class PullChannel(BaseChannel):
    pass


class PushChannel(BaseChannel):
    @deferrable
    def request(self, package):
        sender = self.router.choose(self.socket.get_sender_names(), package)
        socket = self.socket.get_sender_by_name(sender)
        package = self.package_encoder.encode(package)
        return socket.request(package)

    @deferrable
    def publish(self, package):
        sender = self.socket.get_broadcast_sender_name()
        socket = self.socket.get_sender_by_name(sender)
        message = self.package_encoder.encode(package)
        return socket.publish(message)
