class Activity(object):
    stream_factory = None
    director_factory = None

    def __init__(self, host, identity):
        self.host = host
        self.identity = identity
        self.director = None

    def initialize(self):
        self.director = self.director_factory(self.identity)

    def start(self):
        router = self.stream_factory.create_router_stream()
        router.message_received.connect(self._read_external_message)
        router.start_on_random_port(self.host)

    def _read_external_message(self, message):
        pass
