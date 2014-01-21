class Starter(object):
    """
    :type logger: L{logging.Logger}
    :type reactor: L{pycloudia.reactor.interfaces.IReactor}
    :type io_loop: L{zmq.eventloop.minitornado.ioloop.IOLoop}
    """

    logger = None
    reactor = None
    io_loop = None

    def start(self):
        try:
            self.io_loop.start()
            self.logger.info('Started')
        except KeyboardInterrupt:
            self.reactor.call_feature('fireSystemEvent', 'shutdown')
            self.reactor.call_feature('disconnectAll')
            self.logger.info('Stopped')
