from abc import ABCMeta, abstractmethod


__all__ = [
    'IStartStreamStrategy',
    'ISendStreamMessageStrategy',
    'IReadStreamMessageStrategy',
]


class IStartStreamStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start_tcp(self, stream, host, port):
        """
        :type stream: L{pycloudia.streams.zmq_impl.streams.BaseStream}
        :type host: C{str}
        :type port: C{int}
        """

    @abstractmethod
    def start_tcp_on_random_port(self, stream, host, *args, **kwargs):
        """
        :type stream: L{pycloudia.streams.zmq_impl.streams.BaseStream}
        :type host: C{str}
        :return: port chosen by random
        :rtype: C{int}
        """


class IReadStreamMessageStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read_message(self, stream, message_list):
        """
        :type stream: L{pycloudia.streams.zmq_impl.streams.BaseStream}
        :type message_list: C{list} of C{str}
        """


class ISendStreamMessageStrategy(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_message(self, stream, message):
        """
        :type stream: L{pycloudia.streams.zmq_impl.streams.BaseStream}
        :type message: L{pycloudia.streams.zmq_impl.messages.Message}
        """
