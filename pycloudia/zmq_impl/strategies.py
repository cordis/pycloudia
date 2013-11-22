class BaseStartStrategy(object):
    ADDRESS_TCP_HOST = 'tcp://{0}'
    ADDRESS_TCP_HOST_PORT = 'tcp://{0}:{1}'

    def start_tcp(self, socket, host, port):
        raise NotImplementedError()

    def start_tcp_on_random_port(self, socket, host):
        raise NotImplementedError()

    def start_tcp_on_interface(self, socket, interface, port):
        raise NotImplementedError()

    def start_tcp_on_interface_and_random_port(self, socket, interface):
        raise NotImplementedError()

    def _create_tcp_host_address(self, host):
        return self.ADDRESS_TCP_HOST.format(host)

    def _create_tcp_host_port_address(self, host, port):
        return self.ADDRESS_TCP_HOST_PORT.format(host, port)


class ConnectStartStrategy(BaseStartStrategy):
    def start_tcp(self, socket, host, port):
        address = self._create_tcp_host_port_address(host, port)
        socket.connect(address)


class BindStartStrategy(BaseStartStrategy):
    def start_tcp(self, socket, host, port):
        address = self._create_tcp_host_port_address(host, port)
        socket.bind(address)

    def start_tcp_on_random_port(self, socket, host, **kwargs):
        address = self._create_tcp_host_address(host)
        socket.bind_to_random_port(address, **kwargs)
