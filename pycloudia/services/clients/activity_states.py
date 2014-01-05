from abc import ABCMeta, abstractmethod

from pycloudia.uitls.defer import inline_callbacks, return_value
from pycloudia.services.clients.consts import HEADER, COMMAND


class BaseState(object):
    __metaclass__ = ABCMeta

    def __init__(self, activity):
        """
        :type activity: C{pycloudia.activities.clients.activity.Activity}
        """
        self.activity = activity

    @abstractmethod
    def process_incoming_package(self, package):
        raise NotImplementedError()


class GuestState(BaseState):
    def process_incoming_package(self, package):
        if self._is_authentication_package(package):
            return self._authenticate(package)
        return self.activity.route_package(package)

    @inline_callbacks
    def _authenticate(self, package):
        user_id, package = yield self.activity.auth.set_user_state(self.activity.client_id, package)
        user_id = yield self.activity.dao.store_user_id(self.activity.client_id, user_id)
        self.activity.set_user_state(user_id)
        return_value(package)

    @staticmethod
    def _is_authentication_package(package):
        return package.headers[HEADER.COMMAND] == COMMAND.AUTHENTICATE


class UserState(BaseState):
    def __init__(self, activity, user_id):
        super(UserState, self).__init__(activity)
        self.user_id = user_id

    def process_incoming_package(self, package):
        package.headers[HEADER.USER_ID] = self.user_id
        return self.activity.route_package(package)
