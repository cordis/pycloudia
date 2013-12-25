from bisect import bisect_left, bisect_right
from zope.interface import implementer

from pycloudia.cloud.interfaces import ISortedSet


@implementer(ISortedSet)
class SortedSet(object):
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
        insert_before_index = bisect_left(self.subject, item)
        insert_after_index = bisect_right(self.subject, item)
        return insert_before_index != insert_after_index

    def index(self, item):
        insert_before_index = bisect_left(self.subject, item)
        insert_after_index = bisect_right(self.subject, item)
        if insert_before_index == insert_after_index:
            raise ValueError('{0!r} not found'.format(item))
        return insert_before_index

    def insert(self, item):
        insert_before_index = bisect_left(self.subject, item)
        insert_after_index = bisect_right(self.subject, item)
        if insert_before_index != insert_after_index:
            raise ValueError('{0!r} not found'.format(item))
        self.subject.insert(insert_before_index, item)

    def remove(self, item):
        index = self.index(item)
        del self.subject[index]
