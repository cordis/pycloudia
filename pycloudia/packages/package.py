from pycloudia.packages.interfaces import IPackage
from pycloudia.packages.consts import PACKAGE
from pycloudia.packages.decoder import Decoder
from pycloudia.packages.encoder import Encoder


class Package(IPackage):
    def __init__(self, content, headers=None):
        self.content = content
        self.headers = headers or {}


class PackageFactory(object):
    """
    :type encoding: C{str}
    :type content_delimiter: C{str}
    :type headers_delimiter: C{str}
    :type package_factory: C{Callable}
    :type encoder_factory: C{Callable}
    :type decoder_factory: C{Callable}
    """
    encoding = PACKAGE.ENCODING
    content_delimiter = PACKAGE.CONTENT_DELIMITER
    headers_delimiter = PACKAGE.HEADERS_DELIMITER
    package_factory = Package
    encoder_factory = Encoder
    decoder_factory = Decoder

    def create_encoder(self):
        instance = self.encoder_factory()
        instance.encoding = self.encoding
        instance.content_delimiter = self.content_delimiter
        instance.headers_delimiter = self.headers_delimiter
        return instance

    def create_decoder(self):
        instance = self.decoder_factory(self)
        instance.content_delimiter = self.content_delimiter
        instance.headers_delimiter = self.headers_delimiter
        return instance

    def __call__(self, content, headers):
        return self.package_factory(content, headers)
