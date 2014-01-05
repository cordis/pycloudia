from pyschema import Schema, Str

from pycloudia.cloud.interfaces import IServiceInvoker, IServiceAdapter
from pycloudia.services.clients.interfaces import IService
from pycloudia.services.clients.consts import HEADER, COMMAND, SERVICE, SOURCE
from pycloudia.uitls.beans import DataBean


class RequestCreateSchema(Schema):
    client_id = Str()
    facade_id = Str()


class RequestDeleteSchema(Schema):
    client_id = Str()
    reason = Str()


class ClientProxy(object, IService, IServiceAdapter):
    def __init__(self, sender):
        """
        :type sender: L{pycloudia.cloud.interfaces.ISender}
        """
        self.sender = sender

    def create_activity(self, client_id, facade_id):
        request = RequestCreateSchema().encode(DataBean(client_id=client_id, facade_id=facade_id))
        package = self.sender.package_factory(request, {
            HEADER.COMMAND: COMMAND.CREATE,
        })
        self.sender.send_package_by_decisive(client_id, SERVICE.NAME, package)

    def delete_activity(self, client_id, reason=None):
        request = RequestDeleteSchema().encode(DataBean(client_id=client_id, reason=reason))
        package = self.sender.package_factory(request, {
            HEADER.COMMAND: COMMAND.DELETE,
        })
        self.sender.send_package_by_decisive(client_id, SERVICE.NAME, package)

    def suspend_activity(self, client_id):
        raise NotImplementedError()

    def restore_activity(self, client_id, facade_id):
        raise NotImplementedError()

    def process_incoming_package(self, client_id, package):
        package.headers[HEADER.SOURCE] = SOURCE.EXTERNAL
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package_by_decisive(client_id, SERVICE.NAME, package)

    def process_outgoing_package(self, client_id, package):
        package.headers[HEADER.SOURCE] = SOURCE.INTERNAL
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package_by_decisive(client_id, SERVICE.NAME, package)


class ServerProxy(object, IServiceInvoker):
    def __init__(self, service):
        """
        :type service: L{pycloudia.activities.clients.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        command = package.headers[HEADER.COMMAND]
        if command == COMMAND.CREATE:
            request = RequestCreateSchema().decode(package.content)
            self.service.create_activity(request.client_id, request.facade_id)
        elif command == COMMAND.DELETE:
            request = RequestDeleteSchema().decode(package.content)
            self.service.delete_activity(request.client_id, request.reason)
        else:
            client_id = package.headers[HEADER.CLIENT_ID]
            source = package.headers[HEADER.SOURCE]
            if source == SOURCE.EXTERNAL:
                self.service.process_incoming_package(client_id, package)
            elif source == SOURCE.INTERNAL:
                self.service.process_outgoing_package(client_id, package)
