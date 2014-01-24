class PackageError(RuntimeError):
    def __init__(self, package, *args, **kwargs):
        self.package = package
        super(PackageError, self).__init__(*args, **kwargs)


class PackageIgnoredWarning(PackageError):
    pass


class InvalidChannelError(ValueError):
    def __init__(self, channel, *args, **kwargs):
        """
        :type channel: L{pycloudia.services.beans.Channel}
        """
        super(InvalidChannelError, self).__init__(*args, **kwargs)
        self.channel = channel
