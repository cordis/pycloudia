from collections import namedtuple

from springpython.config import PythonConfig, Object
from springpython.context import scope

from pycloudia.uitls.abstracts import AbstractRegistry
from pycloudia.nodes import WorkerNode, ConfigNode
from pycloudia.reactor import twisted_impl
from pycloudia.services import config
from pycloudia import channels


class Config(PythonConfig):
    options_factory = namedtuple('ConfigOptions', '''
internal_host
external_host
config_address_list
cluster_name
''')

    def __init__(self, options):
        self.options = options
        super(Config, self).__init__()

    @Object(scope.SINGLETON)
    def config(self):
        instance = self._create_node(ConfigNode)
        instance.config_service_factory = self.node_config_service_factory()
        return instance

    @Object(scope.SINGLETON)
    def worker(self):
        return self._create_node(WorkerNode)

    def _create_node(self, cls):
        instance = ConfigNode(self.options)
        instance.reactor = self.reactor()
        instance.console = self.console()
        instance.runtime_factory = self.node_runtime_factory()
        instance.worker_service_factory = self.node_worker_service_factory()
        return instance

    @Object(scope.SINGLETON)
    def reactor(self):
        return twisted_impl.ReactorAdapter.create_instance()

    @Object(scope.SINGLETON)
    def console(self):
        return None

    @Object(scope.PROTOTYPE)
    def node_runtime_factory(self):
        raise NotImplementedError()

    @Object(scope.SINGLETON)
    def node_config_service_factory(self):
        instance = config.ServiceFactory()
        instance.state_factory = self.node_config_service_state_factory()
        instance.request_factory = self.node_config_service_request_factory()
        instance.processor_factory = self.node_config_service_processor_factory()
        return instance

    @Object(scope.SINGLETON)
    def node_config_service_state_factory(self):
        return config.ServiceStateFactory(self.options)

    @Object(scope.PROTOTYPE)
    def node_config_service_request_factory(self):
        return config.RequestsFactory()

    @Object(scope.PROTOTYPE)
    def node_config_service_processor_factory(self):
        return config.ProcessorsFactory()

    @Object(scope.SINGLETON)
    def socket_factory_registry(self):
        return AbstractRegistry({
            channels.IMPL.ZMQ: self._create_zmq_socket_factory(),
        }, channels.IMPL.ZMQ)

    def _create_zmq_socket_factory(self):
        return channels.txzmq_impl.SocketFactory()
