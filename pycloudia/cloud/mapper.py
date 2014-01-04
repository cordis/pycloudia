from zope.interface import implementer

from pycloudia.cloud.interfaces import ISequenceSpread, ISortedSet, IMapper


@implementer(IMapper)
class Mapper(object):
    sorted_set = ISortedSet
    spread = ISequenceSpread

    def __init__(self, capacity, replicas):
        assert not capacity % replicas
        self.capacity = capacity
        self.replicas = replicas
        self.slot_map = None

    def initialize(self, item):
        self.sorted_set.insert(item)
        self.slot_map = [item for _ in xrange(self.capacity)]

    def attach(self, item):
        self.sorted_set.insert(item)
        return list(self._update_slot_map())

    def detach(self, item):
        self.sorted_set.remove(item)
        return list(self._update_slot_map())

    def _update_slot_map(self):
        item_spread = self.spread.spread(self.sorted_set, self.capacity)
        for slot, item in enumerate(item_spread):
            if self.slot_map[slot] == item:
                continue
            yield self.slot_map[slot], item
            self.slot_map[slot] = item

    def get_item_by_decisive(self, decisive):
        assert groups is None



class MapperFactory(object):
    signal_factory = None
    sorted_set_factory = None
    spread_factory = None

    def __init__(self, capacity, replicas):
        self.capacity = capacity
        self.replicas = replicas

    def __call__(self):
        instance = Mapper(self.capacity, self.replicas)
        instance.sorted_set = self.sorted_set_factory()
        instance.spread = self.spread_factory()
        return instance
