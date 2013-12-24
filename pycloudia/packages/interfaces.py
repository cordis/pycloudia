from zope.interface import Interface, Attribute


class IPackage(Interface):
    content = Attribute(''':type: C{str}''')
    headers = Attribute(''':type: C{dict}''')


class IEncoder(Interface):
    def encode(package):
        """
        :type package: C{IPackage}
        :rtype: C{str}
        :raises: C{pycloudia.packages.exceptions.InvalidEncodingError}
        """


class IDecoder(Interface):
    def decode(message):
        """
        :type message: C{str}
        :rtype: C{IPackage}
        :raises: C{pycloudia.packages.exceptions.InvalidFormatError}
        """
