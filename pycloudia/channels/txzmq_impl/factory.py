from txzmq import ZmqFactory

from pycloudia.channels.consts import METHOD
from pycloudia.channels.txzmq_impl.sockets import *


class SocketFactory(object):
    DEFAULT_PROTOCOL = 'tcp'

    method_to_cls_map = {
        METHOD.DEALER: DealerSocket,
        METHOD.ROUTER: RouterSocket,
        METHOD.PUSH: PushSocket,
        METHOD.SINK: SinkSocket,
        METHOD.BLOW: BlowSocket,
        METHOD.PULL: PullSocket,
        METHOD.PUB: PubSocket,
        METHOD.SUB: SubSocket,
    }

    def __init__(self):
        self.zmq_factory = ZmqFactory()
        self.zmq_factory.registerForShutdown()

    def __call__(self, method, address, *args, **kwargs):
        """
        :type method: C{str}
        :type address: C{pycloudia.utils.net.Address}
        :rtype: C{pycloudia.channels.txzmq_impl.sockets.BaseSocket}
        """
        socket_cls = self.method_to_cls_map[method]
        address = self.create_zmq_address(address)
        return socket_cls(self.zmq_factory, address, *args, **kwargs)

    def create_router(self, address):
        return self(METHOD.ROUTER, address)

    @staticmethod
    def create_zmq_address(address, protocol=DEFAULT_PROTOCOL):
        return '%s://%s:%d' % protocol, address.host, address.port
