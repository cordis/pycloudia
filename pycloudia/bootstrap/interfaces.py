from abc import ABCMeta, abstractmethod


class IDevice(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        pass


class IStarter(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        pass
