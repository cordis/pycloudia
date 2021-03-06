from pycloudia.respondent.runner import Runner
from springpython.config import PythonConfig, Object
from springpython.context import scope

from pycloudia.packages.decoder import Decoder
from pycloudia.packages.encoder import Encoder
from pycloudia.packages.factory import PackageFactory
from pycloudia.channels.factory import ChannelFactory


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
        return Encoder()

    @Object(scope.SINGLETON)
    def package_decoder(self):
        return Decoder(self.package_factory())

    @Object(scope.SINGLETON)
    def package_factory(self):
        return PackageFactory()

    @Object(scope.SINGLETON)
    def respondent(self):
        instance = Runner()
        instance.reactor = self.reactor()
        return instance

    @Object(scope.SINGLETON, lazy_init=True)
    def twisted_zmq_socket_factory(self):
        from pycloudia.channels.txzmq_impl.factory import SocketFactory
        return SocketFactory()
