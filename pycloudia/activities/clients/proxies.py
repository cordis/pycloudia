from zope.interface import implementer

from pyschema import Schema, Str

from pycloudia.cloud.interfaces import IPackageProcessor
from pycloudia.activities.clients.interfaces import IService
from pycloudia.activities.clients.consts import HEADER, COMMAND, ACTIVITY, SOURCE
from pycloudia.uitls.beans import BaseBean


class RequestCreateSchema(Schema):
    client_id = Str()
    facade_id = Str()


class RequestDeleteSchema(Schema):
    client_id = Str()
    reason = Str()


@implementer(IService)
class ClientProxy(object):
    package_factory = None

    def __init__(self, broker):
        self.broker = broker

    def create_activity(self, client_id, facade_id):
        request = RequestCreateSchema().encode(BaseBean(client_id=client_id, facade_id=facade_id))
        package = self.package_factory(request, {
            HEADER.COMMAND: COMMAND.CREATE,
        })
        self.broker.send_package_by_decisive(client_id, ACTIVITY.NAME, package)

    def delete_activity(self, client_id, reason=None):
        request = RequestDeleteSchema().encode(BaseBean(client_id=client_id, reason=reason))
        package = self.package_factory(request, {
            HEADER.COMMAND: COMMAND.DELETE,
        })
        self.broker.send_package_by_decisive(client_id, ACTIVITY.NAME, package)

    def process_incoming_package(self, client_id, package):
        package.headers[HEADER.SOURCE] = SOURCE.EXTERNAL
        package.headers[HEADER.CLIENT_ID] = client_id
        self.broker.send_package_by_decisive(client_id, ACTIVITY.NAME, package)


@implementer(IPackageProcessor)
class ServerProxy(object):
    def __init__(self, service):
        """
        :type service: C{pycloudia.activities.clients.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        resource = package.headers[HEADER.COMMAND]
        if resource == COMMAND.CREATE:
            request = RequestCreateSchema().decode(package.content)
            self.service.create_activity(request.client_id, request.facade_id)
        elif resource == COMMAND.DELETE:
            request = RequestDeleteSchema().decode(package.content)
            self.service.delete_activity(request.client_id, request.reason)
        else:
            client_id = package.headers[HEADER.CLIENT_ID]
            source = package.headers[HEADER.SOURCE]
            if source == SOURCE.EXTERNAL:
                self.service.process_incoming_package(client_id, package)
            elif source == SOURCE.INTERNAL:
                self.service.process_outgoing_package(client_id, package)
