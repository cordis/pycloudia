from pycloudia.consts import PACKAGE


class OnlineMessage(object):
    def __init__(self, worker_id, internal_host, external_host):
        self.worker_id = worker_id
        self.internal_host = internal_host
        self.external_host = external_host

    def create_package_content(self):
        return {
            'internal_host': self.internal_host,
            'external_host': self.external_host,
        }

    def create_package_headers(self):
        return {
            PACKAGE.HEADER.RESOURCE: '/config/init',
            PACKAGE.HEADER.WORKER_ID: self.worker_id,
        }
