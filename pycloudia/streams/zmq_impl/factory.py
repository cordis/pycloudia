from zmq import Context as ZmqContext

from pycloudia.streams.zmq_impl.streams import *


class StreamFactory(object):
    zmq_context = None
    zmq_io_loop = None

    @classmethod
    def create_instance(cls, zmq_io_loop, io_threads=1):
        instance = cls()
        instance.zmq_context = ZmqContext.instance(io_threads)
        instance.zmq_io_loop = zmq_io_loop
        return instance

    def __init__(self):
        self.streams = set()

    def shutdown(self):
        for stream in self.streams.copy():
            self.remove_stream(stream)
        self.streams = None

        self.zmq_context.term()
        self.zmq_context = None

    def remove_stream(self, stream):
        self.streams.discard(stream)
        stream.close()

    def create_request_stream(self, identity):
        raise NotImplementedError()

    def create_response_stream(self):
        raise NotImplementedError()

    def create_router_stream(self):
        return RouterStream.create_instance(self.zmq_context, self.zmq_io_loop)

    def create_dealer_stream(self, identity):
        return DealerStream.create_instance(self.zmq_context, self.zmq_io_loop, identity)

    def create_sink_stream(self):
        return SinkStream.create_instance(self.zmq_context, self.zmq_io_loop)

    def create_push_stream(self, identity):
        return PushStream.create_instance(self.zmq_context, self.zmq_io_loop, identity)

    def create_pull_stream(self):
        return PullStream.create_instance(self.zmq_context, self.zmq_io_loop)

    def create_blow_stream(self):
        return BlowStream.create_instance(self.zmq_context, self.zmq_io_loop)

    def create_sub_stream(self):
        return SubStream.create_instance(self.zmq_context, self.zmq_io_loop)

    def create_pub_stream(self):
        return PubStream.create_instance(self.zmq_context, self.zmq_io_loop)
