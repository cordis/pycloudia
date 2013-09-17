from pycloudia.services.runner import ServiceRunner
from pycloudia.uitls.code import import_class


class ServiceFactory(object):
    service_runner_factory = ServiceRunner

    def __init__(self, config, channels):
        self.config = config
        self.channels = channels

    def __call__(self, bean):
        service_factory_cls = import_class(bean.factory)
        service_factory = service_factory_cls(self.config)
        service = service_factory(**bean.options)
        service_runner = self.service_runner_factory(service)

    def _create_transport(self, bean):
        pass
