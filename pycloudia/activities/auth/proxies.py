from pycloudia.uitls.beans import DataBean
from pycloudia.activities.auth.interfaces import IService
from pycloudia.activities.auth.schemas import RequestAuthenticateSchema


class ClientProxy(IService):
    def __init__(self, sender):
        """
        :type sender: L{pycloudia.cloud.interfaces.ISender}
        """
        self.sender = sender

    def authenticate(self, client_id, platform, access_token):
        request = DataBean(client_id=client_id, platform=platform, access_token=access_token)
        request = RequestAuthenticateSchema().encode(request)
        package = self.sender.package_factory(request)
