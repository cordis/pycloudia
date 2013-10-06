from pycloudia.uitls.defer import inline_callbacks
from pycloudia.channels import IMPL
from pycloudia.channels.declarative import router
from pycloudia.services.config_manager.consts import CHANNEL


class Service(object):
    managers = router(CHANNEL.MANAGERS, impl=IMPL.HTTP)

    def __init__(self, config_service):
        self.config_service = config_service

    @managers.consume
    @inline_callbacks
    def process_manage_request(self, package):
        # @TODO: authentication
        pass
