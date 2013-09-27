from txzmq import ZmqFactory

from pycloudia.channels.consts import METHOD
from pycloudia.channels.txzmq_impl.sockets import *


class SocketFactory(object):
    method_to_cls_map = {
        METHOD.REQUEST: DealerSocket,
        METHOD.RESPOND: RouterSocket,
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

    def __call__(self, name, method, host, port, *args, **kwargs):
        socket_cls = self.method_to_cls_map[method]
        address = self._create_address(host, port)
        return socket_cls(self.zmq_factory, address, *args, **kwargs)

    def _create_address(self, host, port, protocol='tcp'):
        return '%s://%s:%d' % protocol, host, port
