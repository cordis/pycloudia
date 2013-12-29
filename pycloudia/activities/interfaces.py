from zope.interface import Interface


class IActivity(Interface):
    def initialize():
        pass

    def start():
        pass


class IActivityFactory(Interface):
    pass
