from logging import getLogger

from pycloudia.consts import PACKAGE


class InvalidMessageError(RuntimeError):
    pass


class PackageDecoder(object):
    logger = getLogger('pycloudia.packages')

    def decode(self, message, package_factory):
        raw_headers, raw_body = self._extract_headers_and_body(message)
        headers = self._parse_headers(raw_headers)
        return package_factory(raw_body, headers)

    def _extract_headers_and_body(self, message):
        try:
            headers, body = message.split(PACKAGE.DELIMITER, 1)
        except ValueError:
            self.logger.exception('Cant decode message: %s', message)
            return '', ''
        else:
            return headers, body

    def _parse_headers(self, string):
        ret = {}
        for line in string.split('\n'):
            values = line.split(':', 1)
            if len(values) != 2:
                continue
            ret[values[0].strip()] = values[1].strip() or None
        return ret
