from abc import ABCMeta, abstractmethod, abstractproperty


class IPackage(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def content(self):
        """
        :rtype: C{str}
        """

    @abstractproperty
    def headers(self):
        """
        :rtype: C{dict}
        """


class IEncoder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def encode(self, package):
        """
        :type package: C{IPackage}
        :rtype: C{str}
        :raise: L{pycloudia.packages.exceptions.InvalidEncodingError}
        """


class IDecoder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def decode(self, message):
        """
        :type message: C{str}
        :rtype: C{IPackage}
        :raise: L{pycloudia.packages.exceptions.InvalidFormatError}
        """
