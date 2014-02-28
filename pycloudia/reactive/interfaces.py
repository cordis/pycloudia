from abc import ABCMeta


class IReactive(object):
    __metaclass__ = ABCMeta

    reactor = NotImplemented
