from pysigslot import Signal


class BasePeer(object):
    def __init__(self, host, port, identity):
        self.host = host
        self.port = port
        self.identity = identity
        self.on_read = Signal()

    def start(self):
        pass

    def prolongate(self):
        pass

    def send(self, message):
        raise NotImplementedError()


class LocalPeer(BasePeer):
    def send(self, message):
        self.on_read.emit(message)


class RemotePeer(BasePeer):
    dealer = None
    heartbeat = None

    def start(self):
        self.dealer.on_read.connect(self._process_dealer_message)

    def _process_dealer_message(self, message):
        pass

    def prolongate(self):
        self.heartbeat.reset()

    def send(self, message):
        self.dealer.send_message(message)
