from pycloudia.reactor.interfaces import IReactor


class Device(object):
    logger = None
    reactor = IReactor
    explorer = None

    def initialize(self):
        #self.explorer.incoming_stream_created.connect()
        self.reactor.call_when_running(self.explorer.start)
        self.reactor.call_later(15, self._initialize_activities)

    def _initialize_activities(self):
        pass
