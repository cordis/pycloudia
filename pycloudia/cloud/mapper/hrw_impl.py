from copy import copy

from pycloudia.cloud.interfaces import IMapper


class WeightFunction(object):
    large_digest = 1103515245
    small_digest = 12345
    base = 2 ** 31

    def __call__(self, key_int, item_int):
        weight = key_int
        weight = self.large_digest * weight + self.small_digest
        weight ^= item_int
        weight = self.large_digest * weight + self.small_digest
        return weight % self.base


class Mapper(IMapper):
    """
    :type weight_func: C{Callable}
    """
    weight_func = WeightFunction()

    def __init__(self):
        self.current_map = {}
        self.desired_map = {}

    def attach(self, item):
        self.desired_map[item] = hash(item)

    def detach(self, item):
        del self.desired_map[item]

    def balance(self, hashable_list):
        changes_list = []
        for hashable in hashable_list:
            current_item = self._get_item_from_map_by_hashable(self.current_map, hashable)
            desired_item = self._get_item_from_map_by_hashable(self.desired_map, hashable)
            if current_item != desired_item:
                changes_list.append((hashable, current_item, desired_item))
        self.current_map = copy(self.desired_map)
        return changes_list

    def get_item_by_hashable(self, hashable):
        return self._get_item_from_map_by_hashable(self.current_map, hashable)

    def _get_item_from_map_by_hashable(self, item_map, hashable):
        hashable_int = hash(hashable)
        max_weight = 0
        max_index = None
        item_list = item_map.keys()
        for index, item in enumerate(item_list):
            weight = self.weight_func(hashable_int, item_map[item])
            if weight > max_weight:
                max_weight = weight
                max_index = index
        return item_list[max_index]
