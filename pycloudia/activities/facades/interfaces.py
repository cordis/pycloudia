from abc import ABCMeta, abstractmethod, abstractproperty


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_outgoing_package(self, facade_id, client_id, package):
        """
        :type facade_id: C{str}
        :type client_id: C{str}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """


class IListener(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """
        :raises L{pycloudia.activities.facades.exceptions.ListenFailedError}:
        """


class IClient(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def client_id(self):
        """
        :rtype: C{str}
        """

    @abstractmethod
    def send_message(self, message):
        """
        :type message: C{str}
        """


class IClientDirector(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def client_id_factory(self):
        """
        :rtype: C{str}
        """

    @abstractmethod
    def connection_made(self, client):
        """
        :type client: C{IClient}
        """

    @abstractmethod
    def connection_done(self, client):
        """
        :type client: C{IClient}
        """

    @abstractmethod
    def connection_lost(self, client, reason):
        """
        :type client: C{IClient}
        :type reason: C{str}
        """

    @abstractmethod
    def read_message(self, client, message):
        """
        :type client: C{IClient}
        :type str message:
        """

    @abstractmethod
    def send_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
