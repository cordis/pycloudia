from pycloudia.packages import IPackageEncoder
from pycloudia.packages import IPackageDecoder
from pycloudia.cloud.interfaces import ISender, IReader
from pycloudia.cloud.consts import HEADER


class Broker(object, ISender, IReader):
    package_encoder = IPackageEncoder
    package_decoder = IPackageDecoder

    def __init__(self, runner):
        """
        :type runner: L{pycloudia.cloud.interfaces.IRunner}
        """
        self.runner = runner

    def send_package_by_decisive(self, decisive, activity, package):
        package.headers[HEADER.DECISIVE] = decisive
        identity = self.runner.get_identity_by_decisive(decisive, activity)
        self._send_package(identity, activity, package)

    def send_package_by_identity(self, identity, activity, package):
        package.headers[HEADER.IDENTITY] = identity
        self._send_package(identity, activity, package)

    def _send_package(self, identity, activity, package):
        package.headers[HEADER.ACTIVITY] = activity
        message = self.package_encoder.encode(package)
        self.runner.send_message(identity, message)

    def read_message(self, message):
        try:
            package = self.package_decoder.decode(message)
            identity = self.get_identity_from_package(package)
        except (ValueError, KeyError) as e:
            self.logger.exception(e)
        else:
            self.send_package(identity, package)

    def get_identity_from_package(self, package):
        try:
            return package.headers[HEADER.IDENTITY]
        except KeyError:
            decisive = package.headers[HEADER.DECISIVE]
            activity = package.headers[HEADER.ACTIVITY]
            return self.runner.get_identity_by_decisive(decisive, activity)


class BrokerFactory(object):
    package_encoder = IPackageEncoder
    package_decoder = IPackageDecoder

    def __call__(self, runner):
        instance = Broker(runner)
        instance.package_encoder = self.package_encoder
        instance.package_decoder = self.package_decoder
        return instance
