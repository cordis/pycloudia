class Starter(object):
    logger = None
    reactor = None
    io_loop = None

    def start(self):
        try:
            self.io_loop.start()
            self.logger.info('Started')
        except KeyboardInterrupt:
            self.reactor.subject.fireSystemEvent('shutdown')
            self.reactor.subject.disconnectAll()
            self.logger.info('Stopped')
