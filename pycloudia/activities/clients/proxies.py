from pyschema import Schema, Str

from pycloudia.activities.clients.consts import HEADER, RESOURCE, ACTIVITY
from pycloudia.uitls.beans import BaseBean


class RequestCreateSchema(Schema):
    client_id = Str()
    facade_id = Str()


class RequestDeleteSchema(Schema):
    client_id = Str()
    reason = Str()


class ClientProxy(object):
    package_factory = None

    def __init__(self, cloud):
        self.cloud = cloud

    def create_activity(self, client_id, facade_id):
        request = RequestCreateSchema().encode(BaseBean(client_id=client_id, facade_id=facade_id))
        package = self.package_factory(request, {
            HEADER.ACTIVITY: ACTIVITY.NAME,
            HEADER.RESOURCE: RESOURCE.CREATE,
        })
        self.cloud.send_package_by_decisive(client_id, package)

    def delete_activity(self, client_id, reason=None):
        request = RequestDeleteSchema().encode(BaseBean(client_id=client_id, reason=reason))
        package = self.package_factory(request, {
            HEADER.ACTIVITY: ACTIVITY.NAME,
            HEADER.RESOURCE: RESOURCE.DELETE,
        })
        self.cloud.send_package_by_decisive(client_id, package)

    def process_incoming_package(self, client_id, package):
        package.headers[HEADER.ACTIVITY] = ACTIVITY.NAME
        package.headers[HEADER.CLIENT_ID] = client_id
        self.cloud.send_package_by_decisive(client_id, package)


class ServerProxy(object):
    def __init__(self, service):
        self.service = service

    def process_package(self, package):
        resource = package.headers[HEADER.RESOURCE]
        if resource == RESOURCE.CREATE:
            request = RequestCreateSchema().decode(package.content)
            self.service.create_activity(request.client_id, request.facade_id)
        elif resource == RESOURCE.DELETE:
            request = RequestDeleteSchema().decode(package.content)
            self.service.delete_activity(request.client_id, request.reason)
        else:
            client_id = package.headers[HEADER.CLIENT_ID]
            self.service.process_incoming_package(client_id, package)
