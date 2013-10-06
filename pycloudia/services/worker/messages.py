from pycloudia.consts import PACKAGE
from pycloudia.services.config.schemas import InitRequestSchema


class InitMessage(object):
    def __init__(self, host):
        self.host = host

    def create_package_content(self):
        return InitRequestSchema().encode(self)

    def create_package_headers(self):
        return {
            PACKAGE.HEADER.RESOURCE: '/config/init',
        }


class PingMessage(object):
    def create_package_content(self):
        return {}

    def create_package_headers(self):
        return {
            PACKAGE.HEADER.RESOURCE: '/config/ping',
        }
