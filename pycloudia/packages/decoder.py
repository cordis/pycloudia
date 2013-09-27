from logging import getLogger

from pycloudia.consts import PACKAGE


class InvalidMessageError(RuntimeError):
    pass


class PackageDecoder(object):
    logger = getLogger('pycloudia.packages')

    def __init__(self, package_factory):
        self.package_factory = package_factory

    def decode(self, message):
        raw_headers, raw_content = self._extract_headers_and_content(message)
        headers = self._parse_headers(raw_headers)
        return self.package_factory(raw_content, headers)

    def _extract_headers_and_content(self, message):
        try:
            headers, content = message.split(PACKAGE.DELIMITER, 1)
        except ValueError:
            self.logger.exception('Cant decode message: %s', message)
            return '', ''
        else:
            return headers, content

    def _parse_headers(self, string):
        ret = {}
        for line in string.split('\n'):
            values = line.split(':', 1)
            if len(values) != 2:
                continue
            ret[values[0].strip()] = values[1].strip() or None
        return ret
