import sys

from defer import inline_callbacks, return_value, defer as maybe_deferred

from tornado.web import RequestHandler, HTTPError, MissingArgumentError as TornadoMissingArgumentError

from pycloudia.utils.structs import DataBean
from pycloudia.rest.interfaces import IRequest
from pycloudia.rest.exceptions import MissingArgumentError


__all__ = ['GetRequestHandler', 'PostRequestHandler']


class HttpRequest(IRequest):
    def __init__(self, handler, *args, **kwargs):
        """
        :type handler: L{pycloudia.rest.tornado_impl.handlers.BaseRequestHandler}
        """
        self.handler = handler
        if args:
            self.path = args
        else:
            self.path = DataBean(**kwargs)

    def get_argument(self, type_func, name, default=IRequest.MISSED):
        if issubclass(type_func, (tuple, list)):
            method = self.handler.get_arguments
        else:
            method = self.handler.get_argument
        if default is IRequest.MISSED:
            try:
                value = method(name)
            except TornadoMissingArgumentError:
                raise MissingArgumentError(name)
        else:
            value = method(name, default)
        return type_func(value)


class BaseRequestHandler(RequestHandler):
    func = None
    spec = None

    def initialize(self, func, spec):
        """
        :type func: C{Callable}
        :type spec: L{pycloudia.rest.spec.Spec}
        """
        self.func = func
        self.spec = spec

    @inline_callbacks
    def _invoke(self, *args, **kwargs):
        """
        :rtype: L{defer.Deferred} of C{unicode}
        """
        request = self._create_request(*args, **kwargs)
        try:
            response = yield maybe_deferred(self.func, request)
        except Exception as e:
            exc_info = sys.exc_info()
            try:
                resolver = self.spec.resolve_exception(e)
            except LookupError:
                raise e
            else:
                if not isinstance(resolver, callable):
                    status_code, message = resolver
                    raise HTTPError(status_code, e, reason=message)
                response = resolver(e, exc_info)
        response = yield maybe_deferred(self.spec.render, request, response)
        return_value(response)

    def _create_request(self, *args, **kwargs):
        return HttpRequest(self, *args, **kwargs)


class GetRequestHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self._invoke(*args, **kwargs).add_callback(self.finish)


class PostRequestHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        self._invoke(*args, **kwargs).add_callback(self.finish)
