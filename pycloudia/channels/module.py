from springpython.config import PythonConfig, Object
from springpython.context import scope

from pycloudia.packages.decoder import PackageDecoder
from pycloudia.packages.encoder import PackageEncoder
from pycloudia.packages.factory import PackageFactory
from pycloudia.channels.factory import ChannelFactory
from pycloudia.channels.responder import Responder


class ChannelsModule(PythonConfig):
    def __init__(self, reactor, internal_host, external_host):
        self._reactor = reactor
        self.internal_host = internal_host
        self.external_host = external_host
        super(ChannelsModule, self).__init__()

    @Object(scope.SINGLETON)
    def reactor(self):
        return self._reactor

    @Object(scope.SINGLETON)
    def channel_factory(self):
        instance = ChannelFactory(self.internal_host, self.external_host)
        instance.package_decoder = self.package_decoder()
        instance.package_encoder = self.package_encoder()
        return instance

    @Object(scope.SINGLETON)
    def package_encoder(self):
        return PackageEncoder()

    @Object(scope.SINGLETON)
    def package_decoder(self):
        return PackageDecoder(self.package_factory())

    @Object(scope.SINGLETON)
    def package_factory(self):
        return PackageFactory()

    @Object(scope.SINGLETON)
    def responder(self):
        instance = Responder()
        instance.reactor = self.reactor()
        return instance

    @Object(scope.SINGLETON, lazy_init=True)
    def twisted_zmq_socket_factory(self):
        from pycloudia.channels.txzmq_impl.factory import SocketFactory
        return SocketFactory()
