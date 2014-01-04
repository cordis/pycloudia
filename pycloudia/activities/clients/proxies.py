from zope.interface import implementer

from pyschema import Schema, Str

from pycloudia.cloud.interfaces import IServiceInvoker, IServiceAdapter
from pycloudia.activities.clients.interfaces import IService
from pycloudia.activities.clients.consts import HEADER, COMMAND, SERVICE, SOURCE
from pycloudia.uitls.beans import BaseBean


class RequestCreateSchema(Schema):
    client_id = Str()
    facade_id = Str()


class RequestDeleteSchema(Schema):
    client_id = Str()
    reason = Str()


@implementer(IService, IServiceAdapter)
class ClientProxy(object):
    name = SERVICE.NAME
    package_factory = None

    def __init__(self, sender):
        """
        :type sender: L{pycloudia.cloud.interfaces.ISender}
        """
        self.sender = sender

    def create_activity(self, client_id, facade_id):
        return self.sender.create_activity(self.name, client_id, client_id, facade_id)

    def delete_activity(self, client_id, reason=None):
        return self.sender.delete_activity(self.name, client_id, client_id, reason)

    def suspend_activity(self, client_id):
        return self.sender.suspend_activity(self.name, client_id)

    def recover_activity(self, client_id, facade_id):
        return self.sender.recover_activity(self.name, client_id, facade_id)

    def process_incoming_package(self, client_id, package):
        package.headers[HEADER.SOURCE] = SOURCE.EXTERNAL
        package.headers[HEADER.CLIENT_ID] = client_id
        return self.sender.send_package_by_decisive(client_id, SERVICE.NAME, package)

    def process_outgoing_package(self, client_id, package):
        package.headers[HEADER.SOURCE] = SOURCE.INTERNAL
        package.headers[HEADER.CLIENT_ID] = client_id
        return self.sender.send_package_by_decisive(client_id, SERVICE.NAME, package)


@implementer(IServiceInvoker)
class ServerProxy(object):
    def __init__(self, service):
        """
        :type service: L{pycloudia.activities.clients.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        command = package.headers[HEADER.COMMAND]
        if command == COMMAND.CREATE:
            request = RequestCreateSchema().decode(package.content)
            return self.service.create_activity(request.client_id, request.facade_id)
        if command == COMMAND.DELETE:
            request = RequestDeleteSchema().decode(package.content)
            return self.service.delete_activity(request.client_id, request.reason)
        client_id = package.headers[HEADER.CLIENT_ID]
        source = package.headers[HEADER.SOURCE]
        if source == SOURCE.EXTERNAL:
            return self.service.process_incoming_package(client_id, package)
        if source == SOURCE.INTERNAL:
            return self.service.process_outgoing_package(client_id, package)
        raise NotImplementedError()
