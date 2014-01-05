from pycloudia.uitls.defer import maybe_deferred, inline_callbacks, return_value
from pycloudia.services.clients.consts import HEADER
from pycloudia.services.clients.exceptions import UserIdNotFoundError
from pycloudia.services.clients.activity_states import GuestState, UserState, BaseState


class Activity(object):
    logger = None
    facades = None
    auth = None
    users = None
    dao = None
    state = BaseState
    router = None

    def __init__(self, client_id, facade_id):
        self.client_id = client_id
        self.facade_id = facade_id

    @maybe_deferred
    def process_incoming_package(self, package):
        package.headers[HEADER.CLIENT_ID] = self.client_id
        return self.state.process_incoming_package(package)

    @maybe_deferred
    def route_package(self, package):
        return self.router.route_package(package)

    @maybe_deferred
    def process_outgoing_package(self, package):
        package.headers.pop(HEADER.CLIENT_ID, None)
        self.facades.process_outgoing_package(self.facade_id, self.client_id, package)


class ActivityFactory(object):
    logger = None
    router = None
    facade = None
    auth = None
    dao = None

    @maybe_deferred
    def create(self, client_id, facade_id):
        instance = Activity(client_id, facade_id)
        instance = self._inject_dependencies(instance)
        instance.state = GuestState(instance)
        return instance

    @inline_callbacks
    def recover(self, client_id, facade_id):
        instance = Activity(client_id, facade_id)
        instance = self._inject_dependencies(instance)
        try:
            user_id = yield self.dao.find_user_id(client_id)
        except UserIdNotFoundError:
            instance.state = GuestState(instance)
        else:
            instance.state = UserState(instance, user_id)
        return_value(instance)

    def _inject_dependencies(self, instance):
        instance.logger = self.logger
        instance.router = self.router
        instance.facade = self.facade
        instance.auth = self.auth
        instance.dao = self.dao
        return instance
