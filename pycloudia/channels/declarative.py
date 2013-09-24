import collections
import functools

from pycloudia.defer import DeferredListFactory, maybe_deferred
from pycloudia.channels.consts import METHOD


__all__ = ['dealer', 'router', 'push', 'sink', 'blow', 'pull', 'publish', 'subscribe']


ChannelOptions = collections.namedtuple('BaseChannelOptions', '''
name
impl
internal
external
''')


class ChannelDeclaration(object):
    bridge = None
    listeners = []

    def __init__(self, name, impl=None, internal=True, external=False):
        assert internal or external
        self.options = ChannelOptions(name, impl, internal, external)

    def listen(self, func):
        self.listeners.append(func)

    def _decorate_or_proxy(self, method_name, func_or_package, *args, **kwargs):
        method = getattr(self.bridge, method_name)

        if callable(func_or_package):
            wrapper = functools.wraps(func_or_package)
            return wrapper(method)
        else:
            return method(func_or_package, *args, **kwargs)

    def set_bridge(self, bridge):
        self.bridge = bridge
        self.bridge.set_callback(self._callback)

    def _callback(self, package, *args, **kwargs):
        deferred_list = []
        for listener in self.listeners:
            deferred_list.append(maybe_deferred(listener, package, *args, **kwargs))
        return DeferredListFactory.create_all_or_nothing(deferred_list)


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
