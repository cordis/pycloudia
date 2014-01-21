from pycloudia.bootstrap.interfaces import IDevice


class Device(IDevice):
    """
    :type logger: L{logging.Logger}
    :type reactor: L{pycloudia.reactor.interfaces.IReactor}
    :type explorer: L{pycloudia.explorer.interfaces.IRunner}
    """
    logger = None
    reactor = None
    explorer = None

    def initialize(self):
        #self.explorer.incoming_stream_created.connect()
        self.reactor.call_when_running(self.explorer.start)
        self.reactor.call_later(15, self._initialize_activities)

    def _initialize_activities(self):
        pass
