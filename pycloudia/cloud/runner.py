from pysigslot import Signal

from pycloudia.packages import IPackageEncoder
from pycloudia.packages import IPackageDecoder


class Runner(object):
    logger = None
    decisive_header = None
    package_encoder = IPackageEncoder
    package_decoder = IPackageDecoder

    def __init__(self):
        self.incoming_stream = None
        self.outgoing_stream_map = {}
        self.on_package = Signal()

    def attach_incoming_stream(self, stream):
        if self.incoming_stream is not None:
            raise KeyError('Incoming stream {1} already attached'.format(self.incoming_stream.identity))
        self.incoming_stream = stream
        self.incoming_stream.message_received.connect(self._read_message)

    def _read_message(self, message):
        try:
            package = self.package_decoder.decode(message)
            decisive = package.headers[self.decisive_header]
        except (ValueError, KeyError) as e:
            self.logger.exception(e)
        else:
            if self.is_outgoing(decisive):
                raise NotImplementedError()
            else:
                self.on_package.emit(package)

    def is_outgoing(self, decisive):
        return not decisive

    def attach_outgoing_stream(self, stream):
        pass

    def detach_outgoing_stream(self, stream):
        pass

    def send_package(self, package):
        decisive = package.headers[self.decisive_header]
        if not self.is_outgoing(decisive):
            self.on_package.emit(package)
        else:
            stream = self._select_stream(decisive)
            message = self.package_encoder.encode(package)
            message = stream.encode_message_string(message)
            stream.send_message(message)

    def _select_stream(self, decisive):
        raise NotImplementedError(decisive)


class RunnerFactory(object):
    logger = None
    decisive_header = None
    package_encoder = IPackageEncoder
    package_decoder = IPackageDecoder

    def __call__(self):
        instance = Runner()
        instance.logger = self.logger
        instance.package_encoder = self.package_encoder
        instance.package_decoder = self.package_decoder
        return instance
