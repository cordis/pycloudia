from abc import ABCMeta, abstractmethod, abstractproperty


class IRequest(object):
    __metaclass__ = ABCMeta

    MISSED = object()

    @abstractmethod
    def get_argument(self, type_func, name, default=MISSED):
        """
        :type type_func: C{Callable} or C{None}
        :type name: C{str}
        :type default: C{object} or C{None}
        :rtype: C{type_func}
        :raise: L{pycloudia.rest.exceptions.MissingArgumentError}
        """
