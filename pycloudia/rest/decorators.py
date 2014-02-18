from functools import wraps
from defer import inline_callbacks, defer, return_value

try:
    import simplejson as json
except ImportError:
    import json

from tornado.web import HTTPError, RequestHandler

from pycloudia.utils.decorators import generate_list, generate_dict

__all__ = ['rest', 'jsonify']

http_method_list = ['head', 'get', 'post', 'delete', 'patch', 'put', 'options']


class Rest(object):
    @staticmethod
    def handler(cls):
        """
        :type cls: C{type}
        :rtype: C{RequestHandlerDecorator}
        """
        @wraps(cls)
        class RequestHandlerDecorator(RequestHandler):
            subject = None

            def prepare(self):
                self.subject = cls()
                self.subject.request = self

            def __getattr__(self, method):
                if not hasattr(self.subject, method):
                    return getattr(super(RequestHandlerDecorator, self), method)

                if method not in http_method_list:
                    return getattr(self.subject, method)

                def method_decorator(*args, **kwargs):
                    deferred = defer(getattr(self.subject, method), *args, **kwargs)
                    deferred.add_callbacks(self._send_success, self._send_failure)

                return method_decorator

            def _send_success(self, response):
                self.finish(json.dumps({
                    'data': response,
                    'code': 0,
                    'message': None,
                }))

            def _send_failure(self, exception):
                self.finish(json.dumps({
                    'data': None,
                    'code': self._get_failure_code(exception),
                    'message': str(exception),
                }))

            @staticmethod
            def _get_failure_code(exception):
                if isinstance(exception, HTTPError):
                    return exception.status_code
                return getattr(exception, 'code', 500)

        return RequestHandlerDecorator

    @staticmethod
    def error(exception_cls, code, reason=None):
        """
        :type exception_cls: C{type}
        :type code: C{int}
        """
        def http_error_call(func):
            @wraps(func)
            def http_error_decorator(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except exception_cls as e:
                    raise HTTPError(code, e, reason=reason)
            return http_error_decorator
        return http_error_call


class Jsonifier(object):
    @staticmethod
    def item(encode_func):
        """
        :type encode_func: C{Callable}
        """
        def http_jsonify_call(func):
            @wraps(func)
            @inline_callbacks
            def http_jsonify_decorator(*args, **kwargs):
                obj = yield defer(func, *args, **kwargs)
                return_value(encode_func(obj))
            return http_jsonify_decorator

        return http_jsonify_call

    @staticmethod
    def list(encode_func):
        """
        :type encode_func: C{Callable}
        """
        @generate_list
        def encode_list(obj_list):
            for obj in obj_list:
                yield encode_func(obj)

        def http_jsonify_list_call(func):
            @wraps(func)
            @inline_callbacks
            def http_jsonify_list_decorator(*args, **kwargs):
                obj_list = yield defer(func, *args, **kwargs)
                return_value(encode_list(obj_list))
            return http_jsonify_list_decorator

        return http_jsonify_list_call

    @staticmethod
    def dict(encode_func):
        """
        :type encode_func: C{Callable}
        """
        @generate_dict
        def encode_dict(obj_dict):
            for key, obj in obj_dict.iteritems():
                yield key, encode_func(obj)

        def http_jsonify_dict_call(func):
            @wraps(func)
            @inline_callbacks
            def http_jsonify_dict_decorator(*args, **kwargs):
                obj_dict = yield defer(func, *args, **kwargs)
                return_value(encode_dict(obj_dict))
            return http_jsonify_dict_decorator

        return http_jsonify_dict_call


jsonify = Jsonifier()
rest = Rest()
