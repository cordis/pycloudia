from pycloudia.channels.consts import METHOD


class SocketFactory(object):
    reactor = None

    method_to_cls_map = {
        METHOD.SINK: SinkSocket,
        METHOD.BLOW: BlowSocket,
    }

    def __init__(self):
        pass

    def __call__(self, name, method, host, port, *args, **kwargs):
        socket_cls = self.method_to_cls_map[method]
        address = self._create_address(host, port)
        return socket_cls(self.zmq_factory, address, *args, **kwargs)

    def _create_address(self, host, port, protocol='tcp'):
        return '%s://%s:%d' % protocol, host, port
