from zope.interface import Interface


class ReactorInterface(Interface):
    def register_for_shutdown(func):
        pass

    def call_when_running(func):
        pass

    def run():
        pass

    def call(func, *args, **kwargs):
        pass

    def call_later(seconds, func, *args, **kwargs):
        pass
