from pycloudia.utils.code import instantiate_by_config


class ChannelConfigurator(object):
    def __init__(self, min_port=10001, max_port=11024):
        self.min_port = int(min_port)
        self.max_port = int(max_port)


class ChannelConfiguratorBuilder(object):
    channel_configurator_cls = ChannelConfigurator

    def build(self, config=None):
        return self._instantiate_channel_configurator(config)

    def _instantiate_channel_configurator(self, config):
        return instantiate_by_config(self.channel_configurator_cls, config)
