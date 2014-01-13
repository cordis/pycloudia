class ResponderError(RuntimeError):
    def __init__(self, request_id, *args, **kwargs):
        self.request_id = request_id
        super(ResponderError, self).__init__(*args, **kwargs)


class ResponderTimeoutError(ResponderError):
    pass


class ResponderNotFoundError(ResponderError):
    pass


class PackageError(RuntimeError):
    def __init__(self, package, *args, **kwargs):
        self.package = package
        super(PackageError, self).__init__(*args, **kwargs)


class PackageIgnoredWarning(PackageError):
    pass
