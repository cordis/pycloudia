from pycloudia.activities.clients.consts import HEADER
from pycloudia.activities.clients.exceptions import ActivityNotFoundError, HeaderNotFoundError


class Router(object):
    activity_map = None

    def route_package(self, package):
        activity = self._get_header(package, HEADER.ACTIVITY)
        resource = self._get_header(package, HEADER.RESOURCE)
        try:
            return self.activity_map[activity].route_package(resource, package)
        except KeyError:
            raise ActivityNotFoundError(package, activity)

    @staticmethod
    def _get_header(package, header):
        try:
            return package.get_header(header)
        except KeyError:
            raise HeaderNotFoundError(package, header)
