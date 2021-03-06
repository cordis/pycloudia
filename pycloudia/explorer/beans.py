from pycloudia.explorer.interfaces import IAgentConfig
from pycloudia.utils.structs import DataBean


class Peer(DataBean):
    stream = None
    identity = None
    heartbeat = None


class Config(DataBean, IAgentConfig):
    host = None
    min_port = None
    max_port = None
    identity = None
