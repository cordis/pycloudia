from pycloudia.packages.consts import PACKAGE
from pycloudia.packages.decoder import Decoder
from pycloudia.packages.encoder import Encoder


class PackageFactory(object):
    encoding = PACKAGE.ENCODING
    content_delimiter = PACKAGE.CONTENT_DELIMITER
    headers_delimiter = PACKAGE.HEADERS_DELIMITER
    package_factory = None
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
