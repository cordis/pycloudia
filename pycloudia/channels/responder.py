__all__ = ['Responder', 'BaseResponderError', 'RequestTimeoutError', 'ResponderNotFoundError']


class BaseResponderError(RuntimeError):
    def __init__(self, request_id, *args, **kwargs):
        self.request_id = request_id
        super(BaseResponderError, self).__init__(*args, **kwargs)


class RequestTimeoutError(BaseResponderError):
    pass


class ResponderNotFoundError(BaseResponderError):
    pass


class Responder(object):
    reactor = None

    def __init__(self):
        self.registry = {}

    def listen(self, request_id, deferred):
        assert request_id not in self.registry
        self.registry[request_id] = deferred
        self.reactor.call_later(self.reject, request_id)
        return deferred

    def reject(self, request_id):
        try:
            deferred = self.registry.pop(request_id)
        except KeyError:
            pass
        else:
            deferred.errback(RequestTimeoutError(request_id))

    def resolve(self, request_id, *args, **kwargs):
        try:
            deferred = self.registry.pop(request_id)
        except KeyError:
            raise ResponderNotFoundError(request_id)
        else:
            deferred.callback(*args, **kwargs)
