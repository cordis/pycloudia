try:
    import simplejson as json
except ImportError:
    import json

from pycloudia.rest.consts import RENDERER, HEADER, CONTENT_TYPE
from pycloudia.rest.exceptions import MissingArgumentError


class Spec(object):
    def __init__(self):
        self.http_method = None
        self.resource = None
        self.renderer = None
        self.exception_list = []

    def resolve_exception(self, e):
        """
        :type e: C{Exception}
        :rtype: C{tuple} or C{Callable}
        :raise: C{LookupError}
        """
        for exception_resolver in self.exception_list:
            if isinstance(e, exception_resolver[0]):
                if len(exception_resolver) == 2:
                    return exception_resolver[2]
                return exception_resolver[1:]
        raise LookupError()

    def render(self, request, response):
        """
        :type request: L{pycloudia.rest.interfaces.IRequest}
        :type response: C{object}
        :rtype: C{str}
        """
        if self.renderer[0] in [RENDERER.JSONP, RENDERER.JSON]:
            response = json.dumps(response)
        if self.renderer[0] is RENDERER.JSONP:
            try:
                argument = self.renderer[1]
                callback = request.get_argument(str, argument)
            except (KeyError, MissingArgumentError):
                return response, {
                    HEADER.ACCESS_CONTROL_ALLOW_ORIGIN: '*',
                    HEADER.CONTENT_TYPE: CONTENT_TYPE.JSON,
                }
            else:
                response = '{0}({1});'.format(callback, response)
                return response, {
                    HEADER.CONTENT_TYPE: CONTENT_TYPE.JAVASCRIPT,
                }
        return response, {
            HEADER.CONTENT_TYPE: CONTENT_TYPE.JSON,
        }
