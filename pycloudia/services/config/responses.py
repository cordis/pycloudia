from pycloudia.services.config.schemas import InitResponseSchema


class PingResponse(object):
    def to_package(self, package_factory):
        return package_factory({})


class InitResponse(object):
    def __init__(self, config):
        self.config = config

    def to_package(self, package_factory):
        data = InitResponseSchema().encode(self.config)
        return package_factory(data)
