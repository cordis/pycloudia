from zope.interface import implementer

from pycloudia.explorer.interfaces import IAgentConfig
from pycloudia.uitls.beans import BaseBean


class Peer(BaseBean):
    stream = None
    identity = None
    heartbeat = None


@implementer(IAgentConfig)
class Config(BaseBean):
    host = None
    min_port = None
    max_port = None
    identity = None
