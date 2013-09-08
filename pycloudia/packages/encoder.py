from logging import getLogger

from pycloudia.consts import PACKAGE


class InvalidBodyError(RuntimeError):
    pass


class PackageEncoder(object):
    logger = getLogger('pycloudia.packages')

    def encode(self, package):
        body = package.get_body()
        if not isinstance(body, str):
            raise InvalidBodyError('Package body must be string')

        data = '%s%s%s' % (self._encode_headers(package), PACKAGE.DELIMITER, body)
        try:
            return str(data)
        except UnicodeEncodeError:
            try:
                return data.encode(PACKAGE.ENCODING)
            except UnicodeEncodeError:
                self.logger.exception('Cant encode package: %r', data)
                return ''

    def _encode_headers(self, package):
        return '\n'.join(['%s: %s' % h for h in package.headers.data.iteritems()])
