import logging

from springpython.config import PythonConfig, Object
from springpython.context import scope


class Config(PythonConfig):
    """
    Usage:
        context = ApplicationContext(Config())
        context.get_object('bootstrap')
    """

    def __init__(self, options):
        self.options = options
        super(Config, self).__init__()

    @Object(scope.SINGLETON)
    def bootstrap(self):
        raise NotImplementedError()

    @Object(scope.SINGLETON)
    def starter(self):
        from pycloudia.bootstrap.starter import Starter
        instance = Starter()
        instance.logger = logging.getLogger('pycloudia.bootstrap.starter')
        instance.io_loop = self.io_loop()
        instance.reactor = self.reactor()
        return instance

    @Object(scope.PROTOTYPE)
    def device(self):
        from pycloudia.bootstrap.device import Device
        instance = Device()
        instance.logger = logging.getLogger('pycloudia.bootstrap.device')
        instance.reactor = self.reactor()
        instance.explorer = self.explorer()
        return instance

    @Object(scope.PROTOTYPE)
    def explorer(self):
        config = self.explorer_config()
        factory = self.explorer_factory()
        return factory(config)

    @Object(scope.PROTOTYPE)
    def explorer_config(self):
        from pycloudia.explorer import ExplorerConfig
        return ExplorerConfig(
            host=self.localhost(),
            min_port=self.options.min_port,
            max_port=self.options.max_port,
            identity=self.identity(),
        )

    @Object(scope.SINGLETON)
    def identity(self):
        from uuid import uuid4
        return str(uuid4())

    @Object(scope.SINGLETON)
    def localhost(self):
        from pycloudia.uitls.net import get_ip_address
        if self.options.localhost is not None:
            return self.options.localhost
        return get_ip_address(self.options.interface)

    @Object(scope.SINGLETON)
    def explorer_factory(self):
        from pycloudia.explorer import ExplorerFactory, ExplorerProtocol
        from pycloudia.broadcast.udp import UdpMulticastFactory
        instance = ExplorerFactory()
        instance.logger = logging.getLogger('pycloudia.explorer')
        instance.reactor = self.reactor()
        instance.protocol = ExplorerProtocol()
        instance.stream_factory = self.stream_factory()
        instance.broadcast_factory = UdpMulticastFactory(self.options.udp_host, self.options.udp_port)
        return instance

    @Object(scope.SINGLETON)
    def stream_factory(self):
        from pycloudia.streams.zmq_impl.factory import StreamFactory
        return StreamFactory.create_instance(self.io_loop())

    @Object(scope.PROTOTYPE)
    def isolated_reactor(self):
        from pycloudia.reactor.isolated import IsolatedReactor
        return IsolatedReactor(self.reactor())

    @Object(scope.SINGLETON)
    def reactor(self):
        from tornado.platform.twisted import TornadoReactor
        from pycloudia.reactor.twisted_impl import ReactorAdapter
        return ReactorAdapter(TornadoReactor(self.io_loop()))

    @Object(scope.SINGLETON)
    def io_loop(self):
        from zmq.eventloop.ioloop import IOLoop
        return IOLoop.instance()

    @Object(scope.SINGLETON)
    def package_factory(self):
        from pycloudia.packages.package import PackageFactory
        return PackageFactory()

    @Object(scope.SINGLETON)
    def cluster_runner_factory(self):
        from pycloudia.cluster.runner import RunnerFactory
        instance = RunnerFactory()
        instance.logger = logging.getLogger('pycloudia.cluster.runner')
        instance.reactor = self.reactor()
        instance.mapper_factory = self.cluster_mapper_factory()
        instance.broker_factory = self.cluster_broker_factory()
        return instance

    @Object(scope.SINGLETON)
    def cluster_mapper_factory(self):
        from pycloudia.cluster.mapper.hrw_impl import Mapper
        return Mapper

    @Object(scope.SINGLETON)
    def cluster_broker_factory(self):
        from pycloudia.cluster.broker import BrokerFactory
        instance = BrokerFactory()
        instance.logger = logging.getLogger('pycloudia.cluster.broker')
        instance.package_factory = self.package_factory()
        instance.package_encoder = self.package_factory().create_encoder()
        instance.package_decoder = self.package_factory().create_decoder()
        instance.request_id_factory = self.uuid4_factory()
        instance.respondent = self.respondent()
        return instance

    @Object(scope.SINGLETON)
    def uuid4_factory(self):
        from uuid import uuid4
        return lambda: str(uuid4())

    @Object(scope.PROTOTYPE)
    def respondent(self):
        from pycloudia.respondent.runner import Runner
        return Runner()
