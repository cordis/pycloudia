from pycloudia.devices.consts import DEVICE


__all__ = ['DiscoveryProtocol']


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


class BroadcastBeacon(BaseBeacon):
    def __str__(self):
        return ':'.join([self.prefix, str(self.port), self.identity])


class ImmediateBeacon(BaseBeacon):
    def __str__(self):
        return ':'.join([self.prefix, self.host, str(self.port)])


class DiscoveryProtocol(object):
    prefix = DEVICE.DISCOVERY.PROTOCOL
    broadcast_heartbeat_interval = DEVICE.DISCOVERY.BROADCAST_HEARTBEAT_INTERVAL
    immediate_heartbeat_interval = DEVICE.DISCOVERY.IMMEDIATE_HEARTBEAT_INTERVAL

    broadcast_beacon_cls = BroadcastBeacon
    immediate_beacon_cls = ImmediateBeacon

    def is_beacon(self, message):
        return message.startswith(self.prefix)

    def create_broadcast_beacon_message(self, host, port, identity):
        return str(self._create_beacon(self.broadcast_beacon_cls, host, port, identity))

    def create_immediate_beacon_message(self, host, port, identity):
        return str(self._create_beacon(self.immediate_beacon_cls, host, port, identity))

    def parse_broadcast_beacon_message(self, message, host):
        _, port, identity = message.split(':')
        return self._create_beacon(self.broadcast_beacon_cls, host, port, identity)

    def parse_immediate_beacon_message(self, message, identity):
        _, host, port = message.split(':')
        return self._create_beacon(self.immediate_beacon_cls, host, port, identity)

    def _create_beacon(self, factory, host, port, identity):
        return factory(self.prefix, host, port, identity)
