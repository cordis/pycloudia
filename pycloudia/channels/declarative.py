import collections
import functools

from pycloudia.channels.consts import METHOD


__all__ = ['dealer', 'router', 'push', 'sink', 'blow', 'pull', 'publish', 'subscribe']


ChannelOptions = collections.namedtuple('BaseChannelOptions', '''
name
impl
args
kwargs
''')


class ChannelDeclaration(object):
    def __init__(self, name, impl=None, *args, **kwargs):
        self.options = ChannelOptions(name, impl, args, kwargs)
        self.handler = None
        self.listener = None

    def listen(self, func):
        self.listener = func

    def _decorate_or_proxy(self, method_name, func_or_package, *args, **kwargs):
        method = getattr(self.handler, method_name)

        if callable(func_or_package):
            wrapper = functools.wraps(func_or_package)
            return wrapper(method)
        else:
            return method(func_or_package, *args, **kwargs)

    def set_handler(self, handler):
        self.handler = handler
        self.handler.set_callback(self.listener)


class NoListenBehavior(object):
    def listen(self, *args, **kwargs):
        raise NotImplementedError()


class DealerDeclaration(ChannelDeclaration):
    method = METHOD.REQUEST

    def route(self, package_or_func, *client_id_list):
        return self._decorate_or_proxy('route', package_or_func, *client_id_list)

    def broadcast(self, package_or_func):
        return self._decorate_or_proxy('broadcast', package_or_func)


class RouterDeclaration(ChannelDeclaration):
    method = METHOD.RESPOND

    def route(self, package_or_func, *client_id_list):
        return self._decorate_or_proxy('route', package_or_func, *client_id_list)

    def broadcast(self, package_or_func):
        return self._decorate_or_proxy('broadcast', package_or_func)


class PushDeclaration(ChannelDeclaration, NoListenBehavior):
    method = METHOD.PUSH

    def route(self, package_or_func, *client_id_list):
        return self._decorate_or_proxy('route', package_or_func, *client_id_list)

    def broadcast(self, package_or_func):
        return self._decorate_or_proxy('broadcast', package_or_func)


class SinkDeclaration(ChannelDeclaration):
    method = METHOD.SINK


class BlowDeclaration(ChannelDeclaration, NoListenBehavior):
    method = METHOD.BLOW

    def produce(self, package_or_func):
        return self._decorate_or_proxy('produce', package_or_func)


class PullDeclaration(ChannelDeclaration):
    method = METHOD.PULL


class PubDeclaration(ChannelDeclaration, NoListenBehavior):
    method = METHOD.PUB

    def produce(self, package_or_func):
        return self._decorate_or_proxy('produce', package_or_func)


class SubDeclaration(ChannelDeclaration):
    method = METHOD.SUB


dealer = DealerDeclaration
router = RouterDeclaration
push = PushDeclaration
sink = SinkDeclaration
blow = BlowDeclaration
pull = PullDeclaration
publish = PubDeclaration
subscribe = SubDeclaration
