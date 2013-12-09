from zmq import Context as ZmqContext

from pycloudia.zmq_impl.sockets import *


class SocketFactory(object):
    zmq_context = None
    io_loop = None

    @classmethod
    def create_instance(cls, io_loop, io_threads=1):
        instance = cls()
        instance.zmq_context = ZmqContext(io_threads)
        instance.io_loop = io_loop
        return instance

    def __init__(self):
        self.sockets = set()

    def shutdown(self):
        for socket in self.sockets.copy():
            self.remove_socket(socket)
        self.sockets = None

        self.zmq_context.term()
        self.zmq_context = None

    def remove_socket(self, socket):
        self.sockets.discard(socket)
        socket.clost()

    def create_router_socket(self):
        return RouterSocket.create_instance(self.zmq_context, self.io_loop)

    def create_dealer_socket(self, identity):
        return DealerSocket.create_instance(self.zmq_context, self.io_loop, identity)

    def create_sink_socket(self):
        return SinkSocket.create_instance(self.zmq_context, self.io_loop)

    def create_push_socket(self):
        return PushSocket.create_instance(self.zmq_context, self.io_loop)

    def create_pull_socket(self):
        return PullSocket.create_instance(self.zmq_context, self.io_loop)

    def create_blow_socket(self):
        return BlowSocket.create_instance(self.zmq_context, self.io_loop)

    def create_sub_socket(self):
        return SubSocket.create_instance(self.zmq_context, self.io_loop)

    def create_pub_socket(self):
        return PubSocket.create_instance(self.zmq_context, self.io_loop)
