from pycloudia.utils.structs import DataBean


class Activity(DataBean):
    """
    :type service: C{str}
    :type runtime: C{Hashable}
    :type address: C{object}
    """
    service = None
    runtime = None
    address = None
