import collections
import socket
import fcntl
import struct


__all__ = ['Address', 'get_ip_address']


SIOCGIFADDR = 0x8915


Address = collections.namedtuple('Address', 'host port')


def get_ip_address(interface_name):
    """
    :type interface_name: str
    :rtype: str
    :raise: IOError
    """
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packed_interface = struct.pack('256s', interface_name[:15])
    packed_ip = fcntl.ioctl(connection.fileno(), SIOCGIFADDR, packed_interface)[20:24]
    return socket.inet_ntoa(packed_ip)
