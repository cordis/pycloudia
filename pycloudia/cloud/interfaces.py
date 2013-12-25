from zope.interface import Interface


class ISortedSet(Interface):
    def insert(item):
        """
        :type item: C{object}
        """

    def remove(item):
        """
        :type item: C{object}
        """


class ISequenceSpread(Interface):
    def spread(sequence, capacity):
        """
        :type sequence: C{collections.Sequence}
        :type capacity: C{int}
        :rtype: C{collections.Iterable}
        """
