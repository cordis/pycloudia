from zope.interface import implementer

from pycloudia.activities.facades.interfaces import IService
from pycloudia.activities.facades.consts import ACTIVITY, HEADER
from pycloudia.cloud.interfaces import IPackageProcessor


@implementer(IService)
class ClientProxy(object):
    def __init__(self, broker):
        """
        :type broker: C{pycloudia.cloud.interfaces.IBroker}
        """
        self.broker = broker

    def process_outgoing_package(self, facade_id, client_id, package):
        package.headers[HEADER.FACADE_ID] = facade_id
        package.headers[HEADER.CLIENT_ID] = client_id
        self.broker.send_package_by_identity(facade_id, ACTIVITY.NAME, package)


@implementer(IPackageProcessor)
class ServerProxy(object):
    def __init__(self, service):
        """
        :type service: C{pycloudia.activities.facades.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        facade_id = package.headers[HEADER.FACADE_ID]
        client_id = package.headers[HEADER.CLIENT_ID]
        self.service.process_outgoing_package(facade_id, client_id, package)
