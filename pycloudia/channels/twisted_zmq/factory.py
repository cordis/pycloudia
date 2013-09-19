from txzmq import ZmqFactory

from pycloudia.channels.twisted_zmq.sockets import *


class SocketFactory(object):
    socket_type_to_cls_map = {
        'request': DealerSocket,
        'respond': RouterSocket,
        'push': PushSocket,
        'sink': SinkSocket,
        'blow': BlowSocket,
        'pull': PullSocket,
        'publish': PubSocket,
        'subscribe': SubSocket,
    }

    def __init__(self):
        self.zmq_factory = ZmqFactory()
        self.zmq_factory.registerForShutdown()

    def __call__(self, socket_type, host, port, *args, **kwargs):
        socket_cls = self.socket_type_to_cls_map[socket_type]
        address = self._create_address(host, port)
        return socket_cls(self.zmq_factory, address, *args, **kwargs)

    def _create_address(self, host, port, protocol='tcp'):
        return '%s://%s:%d' % protocol, host, port
