from pycloudia.uitls.defer import inline_callbacks, deferrable
from pycloudia.cluster.exceptions import RequestTimeoutError
from pycloudia.services.facades.exceptions import ClientNotFoundError
from pycloudia.services.gateways.consts import HEADER
from pycloudia.services.gateways.interfaces import IService
from pycloudia.services.gateways.runtime import Runtime


class Service(IService, IActivityFactory):
    """
    :type activities: L{pycloudia.cluster.beans.ActivityRegistry}
    :type facades: L{pycloudia.services.facades.interfaces.IService}
    :type gateway_factory: C{Callable}
    :type router: L{pycloudia.services.gateways.interfaces.IRouter}
    :type dao: L{pycloudia.services.gateways.interfaces.IDao}
    """
    activities = None

    facades = None

    gateway_factory = Runtime
    router = None
    dao = None

    def __init__(self):
        self.runtime_map = {}

    @deferrable
    def initialize(self):
        pass

    @deferrable
    def create_gateway(self, client_id, facade_id):
        gateway = self.gateway_factory(client_id, facade_id)
        self.activities.contain(self, gateway)
        self.runtime_map[client_id] = gateway

    @inline_callbacks
    def suspend_activity(self, client_id, facade_id):
        del self.runtime_map[client_id]

    @inline_callbacks
    def recover_activity(self, client_id, facade_id):
        user_id = yield self.dao.find_user_id_or_none(client_id)
        gateway = self.gateway_factory(client_id, facade_id, user_id)
        self.activities.contain(self, gateway)
        self.runtime_map[client_id] = gateway
        yield self._delete_gateway_if_required(facade_id, client_id)

    @inline_callbacks
    def _delete_gateway_if_required(self, facade_id, client_id):
        try:
            yield self.facades.validate(facade_id, client_id)
        except (RequestTimeoutError, ClientNotFoundError) as e:
            yield self.delete_gateway(client_id, e)

    @deferrable
    def delete_gateway(self, client_id, reason=None):
        activity = self.runtime_map.pop(client_id)
        self.activities.discard(self, activity)

    @inline_callbacks
    def authenticate_gateway(self, client_id, user_id):
        runtime = self.runtime_map[client_id]
        runtime.user_id = yield self.dao.store_user_id(client_id, user_id)

    @deferrable
    def process_incoming_package(self, client_id, package):
        runtime = self.runtime_map[client_id]
        package.headers[HEADER.USER_ID] = runtime.user_id
        package.headers[HEADER.CLIENT_ID] = runtime.client_id
        self.router.route_package(package)

    @deferrable
    def process_outgoing_package(self, client_id, package):
        runtime = self.runtime_map[client_id]
        package.headers.pop(HEADER.USER_ID, None)
        package.headers.pop(HEADER.CLIENT_ID, None)
        self.facades.process_outgoing_package(runtime.facade_id, runtime.client_id, package)
