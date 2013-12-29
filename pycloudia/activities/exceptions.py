class PackageError(RuntimeError):
    def __init__(self, package, *args, **kwargs):
        self.package = package
        super(PackageError, self).__init__(*args, **kwargs)
