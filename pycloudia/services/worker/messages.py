from pycloudia.consts import PACKAGE
from pycloudia.services.config.schemas import InitRequestSchema


class InitMessage(object):
    def __init__(self, internal_host, external_host):
        self.internal_host = internal_host
        self.external_host = external_host

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
