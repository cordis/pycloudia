from abc import ABCMeta, abstractmethod


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process_outgoing_package(self, session, package):
        """
        :type session: L{pycloudia.activities.facades.interfaces.ISession}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :raise: L{pycloudia.activities.facades.exceptions.ClientNotFoundError}
        """


class ISessionRegistry(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self):
        """
        :rtype: L{Deferred} of L{pycloudia.activities.facades.interfaces.ISession}
        """

    @abstractmethod
    def delete(self, session, reason):
        """
        :type session: L{pycloudia.activities.facades.interfaces.ISession}
        :type reason: C{str} or C{None}
        :rtype: L{Deferred}
        """


class ISession(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def none(self):
        pass


class IListener(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, director):
        """
        :type director: L{pycloudia.activities.facades.interfaces.IDirector}
        :raise L{pycloudia.activities.facades.exceptions.ListenFailedError}
        """


class IClientIdFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __call__(self):
        """
        :rtype: C{str}
        """


class IClient(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_message(self, message):
        """
        :type message: C{str}
        """


class IDirector(object):
    __metaclass__ = ABCMeta

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
    def read_package(self, client, package):
        """
        :type client: C{IClient}
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
