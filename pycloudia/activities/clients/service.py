from zope.interface import implementer

from pycloudia.activities.clients.consts import SERVICE
from pycloudia.activities.clients.interfaces import IService


@implementer(IService)
class Service(object):
    name = SERVICE.NAME
    activity_factory = None
    activity_registry = None

    def __init__(self):
        self.activities = {}

    def create_activity(self, client_id, facade_id):
        self.activities[client_id] = self.activity_factory(client_id, facade_id)
        self.activity_registry.register(self.name, client_id, client_id, facade_id)

    def delete_activity(self, client_id, reason=None):
        activity = self.activities.pop(client_id)
        activity.stop(reason)
        self.activity_registry.unregister(self.name, client_id)

    def process_incoming_package(self, client_id, package):
        activity = self.activities[client_id]
        activity.process_incoming_package(package)
