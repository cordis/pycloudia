from pycloudia.services.gateways.consts import HEADER
from pycloudia.services.gateways.exceptions import ActivityNotFoundError, HeaderNotFoundError
from pycloudia.services.gateways.interfaces import IRouter


class Router(IRouter):
    service_map = None

    def route_package(self, package):
        service = self._get_header(package, HEADER.SERVICE)
        command = self._get_header(package, HEADER.COMMAND)
        try:
            return self.service_map[service].route_package(command, package)
        except KeyError:
            raise ActivityNotFoundError(package, service)

    @staticmethod
    def _get_header(package, name):
        try:
            return package.headers[name]
        except KeyError:
            raise HeaderNotFoundError(package, name)
