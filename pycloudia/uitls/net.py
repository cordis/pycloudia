import socket
import fcntl
import struct


SIOCGIFADDR = 0x8915


def get_ip_address(interface_name):
    """
    :param interface_name: str
    :rtype: str
    :raise: IOError
    """
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packed_interface = struct.pack('256s', interface_name[:15])
    packed_ip = fcntl.ioctl(connection.fileno(), SIOCGIFADDR, packed_interface)[20:24]
    return socket.inet_ntoa(packed_ip)
