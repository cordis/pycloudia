from tornado.web import Application, URLSpec

from pycloudia.rest.consts import SPEC_ATTRIBUTE_NAME, METHOD
from pycloudia.rest.tornado_impl.handlers import GetRequestHandler, PostRequestHandler
from pycloudia.utils.decorators import generate_list


class Protocol(object):
    def __init__(self, application):
        self.application = application

    def listen(self, port, host, io_loop):
        self.application.listen(port, host, io_loop=io_loop)


class ProtocolFactory(object):
    """
    :type logger: L{logging.Logger}
    """
    logger = None

    request_handler_map = {
        METHOD.GET: GetRequestHandler,
        METHOD.POST: PostRequestHandler,
    }

    def __init__(self, scope_list):
        self.scope_list = scope_list

    def __call__(self, director):
        """
        :type director: L{pycloudia.activities.facades.interfaces.IDirector}
        :rtype: L{pycloudia.activities.facades.tornado_impl.protocol.Protocol}
        """
        handler_list = self._create_handler_list()
        application = Application(handler_list)
        return Protocol(application)

    @generate_list
    def _create_handler_list(self):
        for handler in self.scope_list:
            for method in self._get_rest_method_list(handler):
                yield self._create_tornado_url_spec(method)

    @staticmethod
    def _get_rest_method_list(handler):
        for method_name in dir(handler):
            method = getattr(handler, method_name)
            if hasattr(method, SPEC_ATTRIBUTE_NAME):
                yield method

    def _create_tornado_url_spec(self, func):
        rest_spec = self._get_spec(func)
        self.logger.debug('Creates tornado URLSpec from %r', rest_spec)
        request_handler = self.request_handler_map[rest_spec.http_method]
        return URLSpec(rest_spec.resource, request_handler, dict(func=func, spec=rest_spec))

    @staticmethod
    def _get_spec(func):
        """
        :rtype: L{pycloudia.rest.spec.Spec}
        """
        return getattr(func, SPEC_ATTRIBUTE_NAME)
