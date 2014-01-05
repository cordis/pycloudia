from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def create_activity(self, client_id, facade_id):
        """
        :type client_id: C{str}
        :type facade_id: C{str}
        """

    @abstractmethod
    def delete_activity(self, client_id, reason=None):
        """
        :type client_id: C{str}
        :type reason: C{str}
        """

    @abstractmethod
    def process_incoming_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.cloud.interfaces.IPackage}
        """

    @abstractmethod
    def process_outgoing_package(self, client_id, package):
        """
        :type client_id: C{str}
        :type package: L{pycloudia.cloud.interfaces.IPackage}
        """


class IDao(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def store_user_id(self, client_id, user_id):
        """
        :type client_id: C{str}
        :type user_id: C{str}
        :rtype: L{Deferred}
        """
