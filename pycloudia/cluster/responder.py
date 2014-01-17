from pycloudia.cluster.exceptions import RequestTimeoutError, ResponderNotFoundError
from pycloudia.cluster.interfaces import IResponder


class Responder(IResponder):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IReactor}
    """
    reactor = None

    def __init__(self):
        self.registry = {}

    def listen(self, request_id, deferred, timeout):
        assert request_id not in self.registry
        self.registry[request_id] = deferred
        self._set_timeout(request_id, timeout)
        return deferred

    def _set_timeout(self, request_id, timeout):
        self.reactor.call_later(timeout, self.reject, request_id, RequestTimeoutError(request_id))

    def reject(self, request_id, reason):
        try:
            deferred = self.registry.pop(request_id)
        except KeyError:
            pass
        else:
            deferred.errback(reason)

    def resolve(self, request_id, *args, **kwargs):
        try:
            deferred = self.registry.pop(request_id)
        except KeyError:
            raise ResponderNotFoundError(request_id)
        else:
            deferred.callback(*args, **kwargs)
