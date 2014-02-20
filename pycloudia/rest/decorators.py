from functools import wraps

from defer import inline_callbacks, defer, return_value

from pycloudia.rest.consts import SPEC_ATTRIBUTE_NAME, METHOD
from pycloudia.rest.spec import Spec
from pycloudia.utils.decorators import generate_list, generate_dict

__all__ = ['rest', 'jsonify']


#@TODO: remove it from here
def _send_success(self, response):
    try:
        import simplejson as json
    except ImportError:
        import json

    self.finish(json.dumps({
        'data': response,
        'code': 0,
        'message': None,
    }))


#@TODO: remove it from here
def _send_failure(self, exception):
    try:
        import simplejson as json
    except ImportError:
        import json
    self.finish(json.dumps({
        'data': None,
        'code': self._get_failure_code(exception),
        'message': str(exception),
    }))


def get_or_create_spec(func):
    """
    :rtype: L{pycloudia.rest.spec.Spec}
    """
    if not hasattr(func, SPEC_ATTRIBUTE_NAME):
        setattr(func, SPEC_ATTRIBUTE_NAME, Spec())
    return getattr(func, SPEC_ATTRIBUTE_NAME)


class Rest(object):
    @staticmethod
    def error(exception_cls, code, reason=None):
        """
        :type exception_cls: C{type}
        :type code: C{int}
        :rtype: C{Callable}
        """
        def decorator(func):
            spec = get_or_create_spec(func)
            spec.error_map[exception_cls] = (code, reason)
        return decorator

    class Handler(object):
        def get(self, resource):
            """
            :type resource: C{str}
            :rtype: C{Callable}
            """
            return self._create_http_method_decorator(METHOD.GET, resource)

        def post(self, resource):
            """
            :type resource: C{str}
            :rtype: C{Callable}
            """
            return self._create_http_method_decorator(METHOD.POST, resource)

        @staticmethod
        def _create_http_method_decorator(http_method, resource):
            """
            :type http_method: C{str}
            :type resource: C{str}
            :rtype: C{Callable}
            """
            def decorator(func):
                spec = get_or_create_spec(func)
                spec.http_method = http_method
                spec.resource = resource
                return func
            return decorator

    handler = Handler()


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
