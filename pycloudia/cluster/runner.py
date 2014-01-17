from pycloudia.cluster.interfaces import IRunner


class Runner(IRunner):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IReactor}
    :type logger: L{logging.Logger}
    :type mapper: L{pycloudia.cluster.interfaces.IMapper}
    :type broker: L{pycloudia.cluster.interfaces.IReader}
    """
    reactor = None
    logger = None
    mapper = None
    broker = None

    def __init__(self):
        self.incoming_stream = None
        self.outgoing_stream_map = {}

    def attach_incoming_stream(self, stream):
        if self.incoming_stream is not None:
            raise KeyError('Incoming stream {0} already attached'.format(self.incoming_stream.identity))
        self.incoming_stream = stream
        self.incoming_stream.message_received.connect(self.broker.read_message)

    def attach_outgoing_stream(self, stream):
        self.outgoing_stream_map[stream.identity] = stream
        self.mapper.attach(stream.identity)
        changes = self.mapper.balance()
        self._process_changes(changes)

    def detach_outgoing_stream(self, stream):
        del self.outgoing_stream_map[stream.identity]
        self.mapper.detach(stream.identity)
        changes = self.mapper.balance()
        self._process_changes(changes)

    def _process_changes(self, changes):
        for activity, source_identity, target_identity in changes:
            raise NotImplementedError('Scalability and Fault-tolerance are handled right here!')

    def send_message(self, identity, message):
        stream = self.outgoing_stream_map[identity]
        message = stream.encode_message_string(message)
        stream.send_message(message)

    def is_outgoing(self, identity):
        return identity != self.incoming_stream.identity

    def get_identity_by_decisive(self, decisive):
        return self.mapper.get_item_by_hashable(decisive)

    def get_service_invoker_by_name(self, name):
        raise NotImplementedError()


class RunnerFactory(object):
    reactor = None
    logger = None
    mapper_factory = None
    broker_factory = None

    def __call__(self):
        instance = Runner()
        instance.reactor = self.reactor
        instance.logger = self.logger
        instance.mapper = self.mapper_factory()
        instance.broker = self.broker_factory(instance)
        return instance
