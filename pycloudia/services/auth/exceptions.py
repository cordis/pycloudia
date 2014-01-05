from pycloudia.cloud.resolver import ResolverMeta, resolve_method
from pycloudia.services.auth.consts import VERBOSE


class AuthenticationFailed(RuntimeError):
    pass


class Resolver(object):
    __metaclass__ = ResolverMeta

    @resolve_method(AuthenticationFailed, verbose=VERBOSE.AUTHENTICATION_FAILED)
    def on_authentication_failed(self, exception):
        pass
