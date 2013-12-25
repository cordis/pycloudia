from zope.interface import implementer

from pycloudia.packages.interfaces import IEncoder
from pycloudia.packages.exceptions import InvalidEncodingError


@implementer(IEncoder)
class Encoder(object):
    encoding = None
    content_delimiter = None
    headers_delimiter = None

    def encode(self, package):
        assert isinstance(package.content, str)
        assert isinstance(package.headers, dict)

        message = self._create_message(package)
        message = self._convert_message(message)
        return message

    def _create_message(self, package):
        return '{headers}{delimiter}{content}'.format(
            headers=self._encode_headers(package.headers),
            content=package.content,
            delimiter=self.delimiter,
        )

    def _convert_message(self, message):
        try:
            return str(message)
        except UnicodeEncodeError:
            try:
                return message.encode(self.encoding)
            except UnicodeEncodeError:
                raise InvalidEncodingError('Unable convert package to {0}'.format(self.encoding))

    def _encode_headers(self, headers):
        return self.headers_delimiter.join([
            '{0}:{1}'.format(name, value)
            for name, value
            in headers.data.iteritems()
        ])
