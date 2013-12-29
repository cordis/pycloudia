from zope.interface import implementer

from pycloudia.activities.facade.interfaces import IProtocol, IProtocolFactory


@implementer(IProtocol)
class Protocol(object):
    def __init__(self, server):
        pass


@implementer(IProtocolFactory)
class ProtocolFactory(object):
    pass
