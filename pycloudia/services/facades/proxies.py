from pycloudia.services.facades.interfaces import IService
from pycloudia.services.facades.consts import SERVICE, HEADER
from pycloudia.cloud.interfaces import IServiceInvoker


class ClientProxy(object, IService):
    def __init__(self, sender):
        """
        :type sender: L{pycloudia.cloud.interfaces.ISender}
        """
        self.sender = sender

    def process_outgoing_package(self, facade_id, client_id, package):
        package.headers[HEADER.FACADE_ID] = facade_id
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package_by_identity(facade_id, SERVICE.NAME, package)


class ServerProxy(object, IServiceInvoker):
    def __init__(self, service):
        """
        :type service: L{pycloudia.activities.facades.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        facade_id = package.headers[HEADER.FACADE_ID]
        client_id = package.headers[HEADER.CLIENT_ID]
        self.service.process_outgoing_package(facade_id, client_id, package)
