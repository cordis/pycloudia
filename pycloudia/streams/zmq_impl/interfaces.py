from zope.interface import Interface


__all__ = [
    'IStartStreamStrategy',
    'ISendStreamMessageStrategy',
    'IReadStreamMessageStrategy',
]


class IStartStreamStrategy(Interface):
    def start_tcp(stream, host, port):
        pass

    def start_tcp_on_random_port(stream, host, *args, **kwargs):
        pass


class IReadStreamMessageStrategy(Interface):
    def read_message(stream, message_list):
        pass


class ISendStreamMessageStrategy(Interface):
    def send_message(stream, message):
        pass
