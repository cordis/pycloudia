from pycloudia.services.clients.consts import HEADER
from pycloudia.services.clients.exceptions import ActivityNotFoundError, HeaderNotFoundError


class Router(object):
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
