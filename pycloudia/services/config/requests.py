from pycloudia.consts import PACKAGE


class PingRequest(object):
    timestamp = int

    @classmethod
    def from_package(cls, package):
        instance = cls()
        instance.timestamp = package.get_header(PACKAGE.HEADER.TIMESTAMP)
        return instance


class InitRequest(PingRequest):
    pass


class RequestsFactory(object):
    resource_to_request_factory_map = {
        '/config/ping': PingRequest.from_package,
        '/config/init': InitRequest.from_package,
    }

    def __call__(self, package):
        return self.resource_to_request_factory_map[package.get_header(PACKAGE.HEADER.RESOURCE)](package)
