class AbstractRegistry(object):
    def __init__(self, instances_map, default=None):
        self.instances_map = instances_map
        self.default = default

    def get(self, item):
        return self[item]

    def __getitem__(self, item):
        if item is None:
            item = self.default
        return self.instances_map[item]


class BiDirectedDict(object):
    def __init__(self):
        self.onward = {}
        self.behind = {}

    def __getitem__(self, item):
        return self.onward[item]

    def __setitem__(self, key, value):
        self.onward[key] = value
        self.behind[value] = key

    def __delitem__(self, key):
        del self.behind[self.onward[key]]
        del self.onward[key]

    def pop(self, key):
        value = self.onward.pop(key)
        del self.behind[value]
        return value
