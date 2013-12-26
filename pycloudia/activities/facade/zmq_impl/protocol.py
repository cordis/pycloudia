from zope.interface import implementer

from pycloudia.activities.facade.interfaces import IProtocol, IProtocolFactory


@implementer(IProtocol)
class Protocol(object):
    pass


@implementer(IProtocolFactory)
class ProtocolFactory(object):
    pass
