class Activity(object):
    pass


class Service(Activity):
    def __init__(self, factory):
        self.instance = factory()

    def get_any(self):
        return self.instance


class Runtime(Activity):
    def __init__(self, factory):
        self.factory = factory


class BaseRegistry(object):
    pass
