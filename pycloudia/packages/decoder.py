from zope.interface import implementer

from pycloudia.packages.exceptions import InvalidFormatError
from pycloudia.packages.interfaces import IDecoder


@implementer(IDecoder)
class Decoder(object):
    content_delimiter = None
    headers_delimiter = None

    def __init__(self, package_factory):
        self.package_factory = package_factory

    def decode(self, message):
        headers_string, content = self._extract_headers_and_content(message)
        headers = self._parse_headers(headers_string)
        return self.package_factory(content, headers)

    def _extract_headers_and_content(self, message):
        try:
            return message.split(self.content_delimiter, 1)
        except ValueError:
            raise InvalidFormatError('Unable decode message: {0}'.format(message))

    def _parse_headers(self, headers_string):
        ret = {}
        for line in headers_string.split(self.headers_delimiter):
            values = line.split(':', 1)
            if len(values) != 2:
                continue
            ret[values[0].strip()] = values[1].strip() or None
        return ret
