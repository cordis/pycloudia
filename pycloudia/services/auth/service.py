from pycloudia.uitls.defer import inline_callbacks, return_value
from pycloudia.services.auth.interfaces import IService


class Service(IService):
    """
    :type reactor: L{pycloudia.reactor.interfaces.IReactor}
    :type adapters: L{pycloudia.services.auth.platforms.interfaces.IAdapterRegistry}
    :type dao: L{pycloudia.services.auth.interfaces.IDao}
    :type users: L{pycloudia.services.users.interfaces.IService}
    """
    reactor = None
    adapters = None
    dao = None
    users = None

    @inline_callbacks
    def authenticate(self, client_id, platform, access_token):
        adapter = self.adapters.get_adapter(platform)
        profile = yield adapter.authenticate(access_token)
        user_id, created = yield self.dao.get_or_create_user(platform, profile)
        if created:
            self.reactor.call(self._retrieve_platform_friends, user_id, platform, profile)
        yield self.users.create_or_update_user_activity(user_id, client_id, platform, profile)
        return_value(profile)

    @inline_callbacks
    def _retrieve_platform_friends(self, user_id, platform, profile):
        adapter = self.adapters.get_adapter(platform)
        profile_list = yield adapter.get_friends(profile)
        yield self.dao.set_user_friends(user_id, platform, profile_list)
