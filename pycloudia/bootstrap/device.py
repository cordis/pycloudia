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
    services = None

    def start(self):
        #self.explorer.incoming_stream_created.connect()
        self.reactor.call_when_running(self.explorer.start)
        self.reactor.call_later(15, self._start_services)

    def _start_services(self):
        for service in self.services:
            service.start()
