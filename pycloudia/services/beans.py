from pycloudia.utils.structs import DataBean


class Channel(DataBean):
    """
    :type service: C{str}
    :type address: C{str}
    :type runtime: C{str}
    """
    service = None
    address = None
    runtime = None
