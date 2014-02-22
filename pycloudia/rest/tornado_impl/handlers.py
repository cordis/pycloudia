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
            content = yield maybe_deferred(self.func, request)
        except Exception as e:
            exception_cls, exception, traceback = sys.exc_info()
            try:
                resolver = self.spec.resolve_exception(e)
            except LookupError:
                raise exception_cls, exception, traceback
            else:
                if not isinstance(resolver, callable):
                    status_code, message = resolver
                    raise HTTPError(status_code, e, reason=message)
                content = resolver(e, exception_cls, exception, traceback)
        content, headers = yield maybe_deferred(self.spec.render, request, content)
        return_value((content, headers))

    def _create_request(self, *args, **kwargs):
        return HttpRequest(self, *args, **kwargs)

    def _finish(self, args):
        """
        :type args: C{tuple} of (C{basestring}, C{dict})
        """
        content, headers = args
        self.write(content)
        for name, value in headers.iteritems():
            self.set_header(name, value)
        self.finish()


class GetRequestHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        self._invoke(*args, **kwargs).add_callback(self._finish)


class PostRequestHandler(BaseRequestHandler):
    def post(self, *args, **kwargs):
        self._invoke(*args, **kwargs).add_callback(self._finish)
