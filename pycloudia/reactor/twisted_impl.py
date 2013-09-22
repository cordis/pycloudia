class ReactorAdapter(object):
    @classmethod
    def create_instance(cls):
        from twisted.internet import reactor
        return cls(reactor)

    def __init__(self, subject):
        self.subject = subject

    def register_for_shutdown(self, method):
        self.subject.addSystemEventTrigger('before', 'shutdown', method)

    def call_when_running(self, method):
        self.subject.callWhenRunning(method)

    def run(self):
        self.subject.run()

    def call_later(self, seconds, method, *args, **kwargs):
        self.subject.callLater(seconds, method, *args, **kwargs)
