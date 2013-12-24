from pysigslot import Signal


class Runner(object):
    logger = None

    def __init__(self):
        self.incoming_stream = None
        self.outgoing_stream_map = {}
        self.message_received = Signal()

    def attach_incoming_stream(self, stream):
        if self.incoming_stream is not None:
            raise KeyError('Incoming stream {1} already attached'.format(self.incoming_stream.identity))
        self.incoming_stream = stream
        self.incoming_stream.message_received.connect(self._read_message)

    def _read_message(self, message):
        pass

    def attach_outgoing_stream(self, stream):
        pass

    def detach_outgoing_stream(self, stream):
        pass


class RunnerFactory(object):
    logger = None

    def __call__(self):
        instance = Runner()
        instance.logger = self.logger
        return instance
