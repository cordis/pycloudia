from pycloudia.services.config.schemas import InitResponseSchema


class PingResponse(object):
    def create_package_content(self):
        return {}

    def create_package_headers(self):
        return {}


class InitResponse(object):
    def __init__(self, worker_id):
        self.worker_id = worker_id

    def create_package_content(self):
        return InitResponseSchema().encode(self)

    def create_package_headers(self):
        return {}
