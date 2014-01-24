from pycloudia.services.beans import Channel
from pycloudia.services.interfaces import IServiceChannelFactory, IChannelsFactory


class ChannelsFactory(IChannelsFactory):
    channel_cls = Channel

    def create_by_address(self, service, address):
        return self.channel_cls(service=service, address=address)

    def create_by_runtime(self, service, runtime):
        return self.channel_cls(service=service, runtime=runtime)


class ServiceChannelFactory(IServiceChannelFactory):
    channels_factory = ChannelsFactory()

    def __init__(self, service):
        """
        :type service: C{str}
        """
        self.service = service

    def create_by_address(self, address):
        return self.channels_factory.create_by_address(self.service, address)

    def create_by_runtime(self, runtime):
        return self.channels_factory.create_by_runtime(self.service, runtime)
