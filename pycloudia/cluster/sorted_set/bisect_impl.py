from bisect import bisect_left

from pycloudia.cluster.interfaces import ISortedSet


class SortedSet(object, ISortedSet):
    """
    Inspired by http://code.activestate.com/recipes/577197-sortedcollection/

    @TODO: tests
    """

    def __init__(self, iterable=()):
        self.subject = sorted(iterable)

    def clear(self):
        self.__init__()

    def copy(self):
        return self.__class__(self)

    def __len__(self):
        return len(self.subject)

    def __getitem__(self, i):
        return self.subject[i]

    def __iter__(self):
        return iter(self.subject)

    def __reversed__(self):
        return reversed(self.subject)

    def __repr__(self):
        return '<{0}> {1!r}'.format(self.__class__.__name__, repr(self.subject))

    def __reduce__(self):
        return self.__class__, (self.subject, )

    def __contains__(self, item):
        _, contains = self._find(item)
        return contains

    def remove(self, item):
        index = self.index(item)
        del self.subject[index]

    def index(self, item):
        index, contains = self._find(item)
        if not contains:
            raise ValueError('{0!r} not found'.format(item))
        return index

    def insert(self, item):
        index, contains = self._find(item)
        if contains:
            raise ValueError('{0!r} already exists'.format(item))
        self.subject.insert(index, item)

    def _find(self, item):
        index = bisect_left(self.subject, item)
        return index, item == self.subject[index]
