class Device(object):
    logger = None
    reactor = None
    explorer = None

    def initialize(self):
        #self.explorer.incoming_stream_created.connect()
        self.reactor.call_when_running(self.explorer.start)
