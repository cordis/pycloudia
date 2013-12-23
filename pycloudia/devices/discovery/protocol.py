from pycloudia.devices.consts import DEVICE


__all__ = ['UdpBeacon', 'ZmqBeacon', 'DiscoveryProtocol']


class BaseBeacon(object):
    def __init__(self, prefix, host, port, identity):
        self.prefix = prefix
        self.host = host
        self.port = port
        self.identity = identity

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return ' '.join([type(self).__name__, self.host, str(self.port), self.identity])


class UdpBeacon(BaseBeacon):
    def __str__(self):
        return ':'.join([self.prefix, str(self.port), self.identity])


class ZmqBeacon(BaseBeacon):
    def __str__(self):
        return ':'.join([self.prefix, self.host, str(self.port)])


class DiscoveryProtocol(object):
    prefix = DEVICE.DISCOVERY.PROTOCOL
    udp_heartbeat_interval = DEVICE.DISCOVERY.UDP_HEARTBEAT_INTERVAL
    zmq_heartbeat_interval = DEVICE.DISCOVERY.ZMQ_HEARTBEAT_INTERVAL

    udp_beacon_cls = UdpBeacon
    zmq_beacon_cls = ZmqBeacon

    def is_beacon(self, message):
        return message.startswith(self.prefix)

    def create_udp_beacon_message(self, host, port, identity):
        return str(self._create_beacon(self.udp_beacon_cls, host, port, identity))

    def create_zmq_beacon_message(self, host, port, identity):
        return str(self._create_beacon(self.zmq_beacon_cls, host, port, identity))

    def parse_udp_beacon_message(self, message, host):
        _, port, identity = message.split(':')
        return self._create_beacon(self.udp_beacon_cls, host, port, identity)

    def parse_zmq_beacon_message(self, message, identity):
        _, host, port = message.split(':')
        return self._create_beacon(self.zmq_beacon_cls, host, port, identity)

    def _create_beacon(self, factory, host, port, identity):
        return factory(self.prefix, host, port, identity)
