from pycloudia.activities.exceptions import PackageError


class ActivityNotFoundError(PackageError):
    pass


class HeaderNotFoundError(PackageError):
    pass
