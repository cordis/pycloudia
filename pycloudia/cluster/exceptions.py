class PackageError(RuntimeError):
    def __init__(self, package, *args, **kwargs):
        self.package = package
        super(PackageError, self).__init__(*args, **kwargs)


class PackageIgnoredWarning(PackageError):
    pass


class InvalidActivityError(ValueError):
    def __init__(self, activity, *args, **kwargs):
        """
        :type activity: L{pycloudia.cluster.beans.Activity}
        """
        super(InvalidActivityError, self).__init__(*args, **kwargs)
        self.activity = activity
