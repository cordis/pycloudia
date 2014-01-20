from pycloudia.respondent.exceptions import ResponseNotHandledError
from pycloudia.uitls.defer import inline_callbacks, deferrable, Deferred
from pycloudia.cluster.exceptions import InvalidActivityError
from pycloudia.cluster.interfaces import ISender, IReader
from pycloudia.cluster.consts import HEADER, DEFAULT


class Broker(ISender, IReader):
    """
    :type logger: L{logging.Logger}
    :type package_factory: C{Callable}
    :type package_encoder: L{pycloudia.packages.IPackageEncoder}
    :type package_decoder: L{pycloudia.packages.IPackageDecoder}
    :type package_wrapper_factory: C{Callable}
    :type request_id_factory: C{Callable}
    :type respondent: L{pycloudia.respondent.interfaces.IRunner}
    """
    logger = None
    package_factory = None
    package_encoder = None
    package_decoder = None
    package_wrapper_factory = None
    request_id_factory = None
    respondent = None

    def __init__(self, runner):
        """
        :type runner: L{pycloudia.cluster.interfaces.IRunner}
        """
        self.runner = runner

    def send_request_package(self, source, target, package, timeout=DEFAULT.REQUEST_TIMEOUT):
        package = self._set_source_headers(package, source)
        package.headers[HEADER.REQUEST_ID] = request_id = self.request_id_factory()
        deferred = self.respondent.listen(request_id, Deferred(), timeout)
        self.send_package(target, package)
        return deferred

    @staticmethod
    def _set_source_headers(package, source):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :type source: L{pycloudia.cluster.beans.Activity}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """
        package.headers[HEADER.SOURCE_SERVICE] = source.service
        if source.address is not None:
            package.headers[HEADER.SOURCE_ADDRESS] = source.address
        elif source.runtime:
            package.headers[HEADER.SOURCE_RUNTIME] = source.runtime
        else:
            raise InvalidActivityError(source)
        return package

    def send_package(self, target, package):
        package = self._set_target_headers(package, target)
        address = self._get_activity_address(target)
        self._send_or_process_package(address, package)

    @staticmethod
    def _set_target_headers(package, target):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :type target: L{pycloudia.cluster.beans.Activity}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """
        package.headers[HEADER.TARGET_SERVICE] = target.service
        if target.address is not None:
            package.headers[HEADER.TARGET_ADDRESS] = target.address
        elif target.runtime:
            package.headers[HEADER.TARGET_RUNTIME] = target.runtime
        else:
            raise InvalidActivityError(target)
        return package

    def _get_activity_address(self, activity):
        """
        :type activity: L{pycloudia.cluster.beans.Activity}
        :rtype: C{object}
        """
        if activity.address is not None:
            return activity.address
        elif activity.runtime is not None:
            return self.runner.get_identity_by_decisive(activity.runtime)
        else:
            raise InvalidActivityError(activity)

    def read_message(self, message):
        try:
            package = self.package_decoder.decode(message)
            address = self._get_address_from_package(package)
        except (ValueError, KeyError) as e:
            self.logger.exception(e)
        else:
            self._send_or_process_package(address, package)

    def _get_address_from_package(self, package):
        try:
            return package.headers[HEADER.TARGET_ADDRESS]
        except KeyError:
            runtime = package.headers[HEADER.TARGET_RUNTIME]
            return self.runner.get_identity_by_decisive(runtime)

    def _send_or_process_package(self, address, package):
        if self.runner.is_outgoing(address):
            return self._send_package(address, package)
        else:
            return self._process_package(package)

    @deferrable
    def _send_package(self, address, package):
        message = self.package_encoder.encode(package)
        self.runner.send_message(address, message)

    @inline_callbacks
    def _process_package(self, package):
        try:
            response_id = package.headers[HEADER.RESPONSE_ID]
        except KeyError:
            self._process_request_package(package)
        else:
            self._process_response_package(response_id, package)

    def _process_request_package(self, request_package):
        service = request_package.headers[HEADER.TARGET_SERVICE]
        invoker = self.runner.get_service_invoker_by_name(service)
        request_package = self._wrap_package(request_package)
        response_package = yield invoker.process_package(request_package)
        if response_package is not None:
            raise NotImplementedError(response_package)

    def _wrap_package(self, package):
        return self.package_wrapper_factory(package)

    def _process_response_package(self, response_id, response_package):
        try:
            self.respondent.resolve(response_id, response_package)
        except ResponseNotHandledError as e:
            self.logger.exception(e)


class BrokerFactory(object):
    """
    :type logger: L{logging.Logger}
    :type package_factory: C{Callable}
    :type package_encoder: L{pycloudia.packages.IPackageEncoder}
    :type package_decoder: L{pycloudia.packages.IPackageDecoder}
    :type package_wrapper_factory: C{Callable}
    :type request_id_factory: C{Callable}
    :type respondent: L{pycloudia.respondent.interfaces.IRunner}
    """
    logger = None
    package_factory = None
    package_encoder = None
    package_decoder = None
    package_wrapper_factory = None
    request_id_factory = None
    respondent = None

    def __call__(self, runner):
        instance = Broker(runner)
        instance.logger = self.logger
        instance.package_factory = self.package_factory
        instance.package_encoder = self.package_encoder
        instance.package_decoder = self.package_decoder
        instance.package_wrapper_factory = self.package_wrapper_factory
        instance.request_id_factory = self.request_id_factory
        instance.respondent = self.respondent
        return instance
