from pycloudia.uitls.defer import inline_callbacks, return_value
from pycloudia.uitls.beans import DataBean
from pycloudia.cloud.interfaces import IServiceInvoker
from pycloudia.cloud.exceptions import PackageIgnoredWarning
from pycloudia.cloud.resolver import resolve_errors
from pycloudia.services.auth.interfaces import IService
from pycloudia.services.auth.consts import HEADER, COMMAND, SERVICE
from pycloudia.services.auth.schemas import AuthenticateRequestSchema, AuthenticateResponseSchema
from pycloudia.services.auth.exceptions import Resolver


class ClientProxy(object, IService):
    name = SERVICE.NAME

    def __init__(self, sender):
        """
        :type sender: L{pycloudia.cloud.interfaces.ISender}
        """
        self.sender = sender

    def authenticate(self, client_id, platform, access_token):
        request = DataBean(client_id=client_id, platform=platform, access_token=access_token)
        request = AuthenticateRequestSchema().encode(request)
        package = self.sender.package_factory(request, {
            HEADER.COMMAND: COMMAND.AUTHENTICATE,
        })
        self.sender.send_package_by_decisive(client_id, self.name, package)


class ServerProxy(object, IServiceInvoker):
    def __init__(self, service):
        """
        :type service: L{pycloudia.services.auth.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        command = package.headers[HEADER.COMMAND]
        if command == COMMAND.AUTHENTICATE:
            return self._process_authenticate_package(package)
        raise PackageIgnoredWarning(package)

    @resolve_errors(Resolver)
    @inline_callbacks
    def _process_authenticate_package(self, package):
        request = AuthenticateRequestSchema().decode(package.content)
        profile = yield self.service.authenticate(request.client_id, request.platform, request.access_token)
        response = self._create_authenticate_response_package(package, profile)
        return_value(response)

    @staticmethod
    def _create_authenticate_response_package(request_package, profile):
        response = AuthenticateResponseSchema().encode(profile)
        return request_package.create_response(response, {
            HEADER.USER_ID: profile.user_id,
        })
