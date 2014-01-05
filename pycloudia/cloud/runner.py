from pycloudia.cloud.interfaces import IRunner


class Runner(object, IRunner):
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
        changes = self.mapper.attach(stream.identity)
        self._process_slot_changes(changes)

    def detach_outgoing_stream(self, stream):
        del self.outgoing_stream_map[stream.identity]
        changes = self.mapper.detach(stream.identity)
        self._process_slot_changes(changes)

    def _process_slot_changes(self, changes):
        """
        @TODO: Scalability and Fault-tolerance are handled right here!
        """
        for oldSlot, newSlot in changes:
            pass

    def send_message(self, identity, message):
        if self.is_outgoing(identity):
            stream = self.outgoing_stream_map[identity]
            message = stream.encode_message_string(message)
            stream.send_message(message)
        else:
            self.broker.read_message(message)

    def is_outgoing(self, identity):
        return identity != self.incoming_stream.identity

    def get_identity_by_decisive(self, decisive, activity):
        groups = self._get_groups_by_activity(activity)
        return self.mapper.get_item_by_decisive(decisive, groups)

    def _get_groups_by_activity(self, activity):
        return None


class RunnerFactory(object):
    logger = None
    mapper_factory = None
    broker_factory = None

    def __call__(self):
        instance = Runner()
        instance.logger = self.logger
        instance.mapper = self.mapper_factory()
        instance.broker = self.broker_factory(instance)
        return instance
