from zope.interface import implementer

from pycloudia.uitls.defer import maybe_deferred
from pycloudia.activities.interfaces import IActivity, IActivityFactory


@implementer(IActivity)
class Activity(object):
    director = None
    protocol = None
    listener = None

    def initialize(self):
        pass

    def start(self):
        self.listener.start_on_random_port()

    @maybe_deferred
    def process_outgoing_package(self, client_id, package):
        return self.director.process_outgoing_package(client_id, package)


@implementer(IActivityFactory)
class ActivityFactory(object):
    stick_to_group('facade')

    director_factory = None
    protocol_factory = None
    listener_factory = None

    def __init__(self, host):
        self.host = host
        self.director = None
        self.protocol = None
        self.listener = None

    def __call__(self, identity):
        instance = Activity()
        instance.director = self.director_factory(identity)
        instance.protocol = self.protocol_factory(self.director)
        instance.listener = self.listener_factory(self.protocol, self.host)
        return instance
