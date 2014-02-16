class Activity(object):
    def __init__(self, factory):
        self.factory = factory


class Service(Activity):
    def get_any(self):
        raise NotImplementedError()


class Runtime(Activity):
    pass


class BaseRegistry(object):
    pass
