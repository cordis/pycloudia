from pycloudia.services.facades.interfaces import IProtocol, IProtocolFactory


class Protocol(object, IProtocol):
    def __init__(self, server):
        pass


class ProtocolFactory(object, IProtocolFactory):
    pass
