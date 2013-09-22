from time import time
from logging import getLogger

from pycloudia.defer import inline_callbacks, maybe_deferred, DeferredListFactory
from pycloudia.decorators import generate_dict


class ChannelsRegistry(object):
    logger = getLogger('pycloudia.channels')

    def __init__(self, channel_factory):
        self.channel_factory = channel_factory
        self.channels_map = None

    def configure(self, bean_list):
        self.channels_map = self._create_channels_map(bean_list)

    @generate_dict
    def _create_channels_map(self, bean_list):
        for bean in bean_list:
            yield self._create_channel_id(bean), self.channel_factory(bean)

    def _create_channel_id(self, bean):
        return bean.name, bean.port

    def run(self):
        deferred_list = []
        for channel in self.channels_map.values():
            deferred_list.append(self._create_deferred_channel_run(channel))
        return DeferredListFactory.create(deferred_list)

    @inline_callbacks
    def _create_deferred_channel_run(self, channel):
        start = time()
        try:
            yield maybe_deferred(channel.run)
        except RuntimeError as e:
            self._log_channel_failure(channel, e)
        else:
            self._log_channel_success(channel, time() - start)

    def _log_channel_failure(self, channel, exception):
        self.logger.error(
            'Channel %s has not been started on %s:%s: %s',
            channel.name,
            channel.host,
            channel.port,
            exception
        )

    def _log_channel_success(self, channel, start_duration):
        self.logger.info(
            'Channel %s started on %s:%s in %.3f seconds',
            channel.name,
            channel.host,
            channel.port,
            start_duration
        )
