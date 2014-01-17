from pycloudia.cluster.consts import HEADER
from pycloudia.cluster.interfaces import IRequestPackage


class PackageContent(object):
    encoder = None
    decoder = None

    def __init__(self, dict_or_str):
        """
        :type dict_or_str: C{dict} or C{str}
        """
        if isinstance(dict_or_str, dict):
            self.decoded = dict_or_str
            self.encoded = None
        else:
            self.decoded = None
            self.encoded = dict_or_str

    def __str__(self):
        self._encode()
        return str(self.encoded)

    def __unicode__(self):
        self._encode()
        return unicode(self.encoded)

    def _encode(self):
        if self.encoded is None:
            self.encoded = self.encoder.encode(self.decoded)

    def __getitem__(self, item):
        self._decode()
        return self.decoded[item]

    def __setitem__(self, key, value):
        self._decode()
        self.decoded[key] = value
        self.encoded = None

    def __delitem__(self, key):
        self._decode()
        del self.decoded[key]
        self.encoded = None

    def _decode(self):
        if self.decoded is None:
            self.decoded = self.decoder.decode(self.encoded)
        return self.decoded


class RequestPackage(IRequestPackage):
    def __init__(self, subject):
        """
        :type subject: L{pycloudia.packages.interfaces.IPackage}
        """
        self.subject = subject

    def content(self):
        return self.subject.content

    def headers(self):
        return self.subject.headers

    def create_response(self, content, headers=None):
        if HEADER.REQUEST_ID not in self.subject.headers:
            return None
        response = type(self.subject)(content, headers)
        response = self._copy_header(response, HEADER.REQUEST_ID, HEADER.RESPONSE_ID)
        response = self._copy_header(response, HEADER.SOURCE_SERVICE, HEADER.TARGET_SERVICE)
        response = self._copy_header(response, HEADER.SOURCE_RUNTIME, HEADER.TARGET_RUNTIME)
        response = self._copy_header(response, HEADER.SOURCE_ADDRESS, HEADER.TARGET_ADDRESS)
        return response

    def _copy_header(self, package, source, target):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        :type source: C{str}
        :type target: C{str}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """
        try:
            package.headers[target] = self.subject.headers[source]
        except KeyError:
            pass
        return package


class RequestPackageFactory(object):
    """
    :type content_encoder: C{Callable}
    :type content_decoder: C{Callable}
    """
    content_encoder = None
    content_decoder = None

    def __call__(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IPackage}
        """
        package.content = PackageContent(package.content)
        package.content.encoder = self.content_encoder
        package.content.decoder = self.content_decoder
        return RequestPackage(package)
