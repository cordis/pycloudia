import collections
import logging
import functools

from pycloudia.defer import DeferredListFactory
from pycloudia.channels.consts import METHOD


__all__ = ['request', 'respond', 'push', 'sink', 'blow', 'pull', 'publish', 'subscribe']


ChannelOptions = collections.namedtuple('BaseChannelOptions', '''
name
topic
dispatcher
impl
internal
external
''')


class ChannelDecorator(object):
    logger = logging.getLogger('pycloudia.channels')

    @classmethod
    def create_decorator(cls, name, topic=None, dispatcher=None, impl=None, internal=True, external=False):
        assert internal or external
        channel_options = ChannelOptions(name, topic, dispatcher, impl, internal, external)

        def decorator(method):
            if isinstance(method, cls):
                instance = method
            else:
                wrapper = functools.wraps(method)
                instance = wrapper(cls(method))

            instance.channels.append(channel_options)
            return instance

        return decorator

    def __init__(self, method):
        self.method = method
        self.channels = []
        self.handlers = []

    def add_handler(self, handler):
        raise NotImplementedError()


class ActiveChannelDecorator(ChannelDecorator):
    handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def __call__(self, package):
        package = self.method(package)
        deferred_list = []
        for handler in self.handlers:
            deferred_list.append(handler.request(package))
        return DeferredListFactory.create(deferred_list)


class PassiveChannelDecorator(ChannelDecorator):
    def add_handler(self, handler):
        handler.set_callback(self.method)

    def __call__(self, package):
        raise AttributeError('Unable to send to passive channel')


class RequestDecorator(ActiveChannelDecorator):
    method = METHOD.REQUEST


class RespondDecorator(PassiveChannelDecorator):
    method = METHOD.RESPOND


class PushDecorator(ActiveChannelDecorator):
    method = METHOD.PUSH


class SinkDecorator(PassiveChannelDecorator):
    method = METHOD.SINK


class BlowDecorator(ActiveChannelDecorator):
    method = METHOD.BLOW


class PullDecorator(PassiveChannelDecorator):
    method = METHOD.PULL


class PubDecorator(ActiveChannelDecorator):
    method = METHOD.PUB


class SubDecorator(PassiveChannelDecorator):
    method = METHOD.SUB


request = RequestDecorator.create_decorator
respond = RespondDecorator.create_decorator
push = PushDecorator.create_decorator
sink = SinkDecorator.create_decorator
blow = BlowDecorator.create_decorator
pull = PullDecorator.create_decorator
publish = PubDecorator.create_decorator
subscribe = SubDecorator.create_decorator
