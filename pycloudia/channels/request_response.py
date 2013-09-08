from bson import ObjectId


class RequestResponseRegistry(object):
    request_id_factory = ObjectId
    reactor = None
    ttl = 10

    def __init__(self):
        self.id_map = {}

    def get(self, request_id):
        return self.id_map.pop(request_id)

    def set(self, deferred):
        request_id = str(self.request_id_factory())
        self.id_map[request_id] = deferred
        self.reactor.call_later(self.ttl, self.expire, request_id)

    def expire(self, request_id):
        try:
            del self.id_map[request_id]
        except KeyError:
            pass
