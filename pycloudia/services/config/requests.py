from pycloudia.consts import PACKAGE
from pycloudia.services.config.schemas import InitRequestSchema


class PingRequest(object):
    timestamp = None

    @classmethod
    def from_package(cls, package):
        instance = cls()
        instance.timestamp = package.get_headers()[PACKAGE.HEADER.TIMESTAMP]
        return instance


class InitRequest(object):
    cluster = None
    has_config = None
    internal_host = None
    external_host = None
    timestamp = None

    @classmethod
    def from_package(cls, package):
        instance = InitRequestSchema(cls).decode(package.get_content())
        instance.cluster = package.get_headers()[PACKAGE.HEADER.CLUSTER]
        instance.timestamp = package.get_headers()[PACKAGE.HEADER.TIMESTAMP]
        return instance


class RequestsFactory(object):
    resource_to_request_factory_map = {
        '/config/ping': PingRequest.from_package,
        '/config/init': InitRequest.from_package,
    }

    def __call__(self, package):
        return self.resource_to_request_factory_map[package.get_header(PACKAGE.HEADER.RESOURCE)](package)
