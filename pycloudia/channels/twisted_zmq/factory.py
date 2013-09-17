from uuid import uuid4
from txzmq import ZmqFactory

from pycloudia.uitls.dsn import DsnParser
from pycloudia.channels.twisted_zmq.sockets import RouterSocket, DealerSocket, SocketPool


class SocketFactory(object):
    dsn_parser = DsnParser({
        'kwargs': {
            'identity': (str, 'identity')
        }
    })
    dsn_protocol_to_socket_cls_map = {
        'router': RouterSocket,
        'dealer': DealerSocket,
    }

    def __init__(self):
        self.zmq_factory = ZmqFactory()
        self.zmq_factory.registerForShutdown()

    def __call__(self, dsn_str_or_list):
        if isinstance(dsn_str_or_list, list):
            return self._create_socket_pool(dsn_str_or_list)
        else:
            return self._create_socket(dsn_str_or_list)

    def _create_socket_pool(self, dsn_list):
        socket_pool = SocketPool()
        for dsn in dsn_list:
            socket_pool.add(self._create_socket(dsn))
        return socket_pool

    def _create_socket(self, dsn):
        dsn_config = self.dsn_parser.parse(dsn)
        socket_cls = self.dsn_protocol_to_socket_cls_map[dsn_config['protocol']]
        address = self._create_address_from_dsn_config(dsn_config)
        identity = self._create_identity_from_dsn_config(dsn_config)
        return socket_cls(self.zmq_factory, address, identity)

    def _create_address_from_dsn_config(self, dsn_config):
        return 'tcp://' + dsn_config['hostname'] + ':' + dsn_config['port']

    def _create_identity_from_dsn_config(self, dsn_config):
        try:
            return dsn_config['kwargs']['identity']
        except KeyError:
            return str(uuid4())


class SocketConfigurator(object):
    dsn_parser = DsnParser()

    def __init__(self, channels_config):
        self.channels_config = channels_config

    def create_config(self):
        pass
