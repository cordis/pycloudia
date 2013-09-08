from pycloudia.defer import deferrable


class ServiceRunner(object):
    def __init__(self, service):
        self.service = service

    def bind(self, host, port):
        pass

    @deferrable
    def run(self):
        return self.service.run()
