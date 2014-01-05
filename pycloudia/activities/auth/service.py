from pycloudia.uitls.defer import inline_callbacks, return_value
from pycloudia.activities.auth.interfaces import IService, IDao
from pycloudia.activities.auth.platforms.interfaces import IAdapterRegistry


class Service(IService):
    reactor = None
    users = None
    adapter_registry = IAdapterRegistry
    dao = IDao

    @inline_callbacks
    def authenticate(self, client_id, platform, access_token):
        adapter = self.adapter_registry.get_adapter(platform)
        profile = yield adapter.authenticate(access_token)
        user_id, created = yield self.dao.get_or_create_user(platform, profile)
        if created:
            self.reactor.call(self._retrieve_platform_friends, user_id, platform, profile)
        yield self.users.create_or_update_activity(user_id, client_id, platform, access_token, profile)
        return_value(user_id)

    @inline_callbacks
    def _retrieve_platform_friends(self, user_id, platform, profile):
        adapter = self.adapter_registry.get_adapter(platform)
        profile_list = yield adapter.get_friends(profile)
        yield self.dao.set_user_friends(user_id, platform, profile_list)
