from pycloudia.uitls.beans import BaseBean


class DeviceConfig(BaseBean):
    host = None
    min_port = None
    max_port = None
    interface = ''
