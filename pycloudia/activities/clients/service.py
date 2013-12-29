class Service(object):
    activity_factory = None

    def __init__(self):
        self.activities = {}

    def create_activity(self, client_id, facade_id):
        self.activities[client_id] = self.activity_factory(client_id, facade_id)

    def delete_activity(self, client_id, reason=None):
        activity = self.activities.pop(client_id)
        activity.stop(reason)

    def process_incoming_package(self, client_id, package):
        activity = self.activities[client_id]
        activity.process_incoming_package(package)
