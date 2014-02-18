from abc import ABCMeta, abstractmethod, abstractproperty


class IRequest(object):
    __metaclass__ = ABCMeta

    MISSED = object()

    @abstractmethod
    def get_argument(self, name, default=MISSED):
        """
        :type name: C{str}
        :type default: C{str} or C{None}
        :rtype: C{str}
        :raise: L{pycloudia.rest.exceptions.MissingArgumentError}
        """

    @abstractmethod
    def get_argument_as_list(self, name, default=MISSED):
        """
        :type name: C{str}
        :type default: C{list}
        :rtype: C{list} of C{str}
        :raise: L{pycloudia.rest.exceptions.MissingArgumentError}
        """


    @abstractproperty
    def path(self):
        """
        :rtype: C{object}
        """
