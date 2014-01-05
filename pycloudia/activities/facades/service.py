from pycloudia.activities.facades.interfaces import IService


class Service(object, IService):
    def __init__(self, activity):
        self.activity = activity

    def process_outgoing_package(self, facade_id, client_id, package):
        assert facade_id == self.activity.facade_id
        self.activity.process_outgoing_package(client_id, package)
