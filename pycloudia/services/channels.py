from pycloudia.services.beans import Channel
from pycloudia.services.interfaces import IChannelsFactory


class ChannelsFactory(IChannelsFactory):
    channel_cls = Channel

    def __init__(self, service):
        """
        :type service: C{str}
        """
        self.service = service

    def create_by_address(self, address):
        return self.channel_cls(service=self.service, address=address)

    def create_by_runtime(self, runtime):
        return self.channel_cls(service=self.service, runtime=runtime)
