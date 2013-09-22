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
