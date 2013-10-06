from zope.interface import Interface


class ConsumeInterface(Interface):
    def consume(func):
        pass


class ProduceInterface(Interface):
    def produce(package):
        pass


class RouteInterface(Interface):
    def route(package):
        pass


class BroadcastInterface(Interface):
    def broadcast(package):
        pass
