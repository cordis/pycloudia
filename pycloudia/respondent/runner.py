from pycloudia.respondent.exceptions import ResponseTimeoutError, ResponseNotHandledError
from pycloudia.respondent.interfaces import IRunner


class Runner(IRunner):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IReactor}
    :type dao: L{pycloudia.respondent.interfaces.IDao}
    """
    reactor = None
    dao = None

    def __init__(self):
        self.registry = {}

    def listen(self, request_id, deferred, timeout):
        assert request_id not in self.registry
        self.registry[request_id] = deferred
        self._set_timeout(request_id, timeout)
        return deferred

    def _set_timeout(self, request_id, timeout):
        self.reactor.call_later(timeout, self.reject, request_id, ResponseTimeoutError(request_id))

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
            raise ResponseNotHandledError(request_id)
        else:
            deferred.callback(*args, **kwargs)
