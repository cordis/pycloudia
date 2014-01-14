from pycloudia.cloud.exceptions import PackageError


class ActivityNotFoundError(PackageError):
    pass


class HeaderNotFoundError(PackageError):
    pass


class UserIdNotFoundError(Exception):
    pass
