from collections import Counter
from itertools import chain, repeat, izip

from zope.interface import implementer

from pycloudia.cloud.interfaces import ISequenceSpread


@implementer(ISequenceSpread)
class SequenceSpread(object):
    @staticmethod
    def spread(sequence, capacity):
        sequence_size = len(sequence)
        small_chunk_size = capacity // sequence_size
        large_chunk_size = small_chunk_size + 1
        large_chunk_count = capacity % sequence_size
        small_chunk_count = sequence_size - large_chunk_count
        chunk_size_list = chain(
            repeat(large_chunk_size, large_chunk_count),
            repeat(small_chunk_size, small_chunk_count)
        )
        item_chunk_size_map = izip(sequence, chunk_size_list)
        return Counter(dict(item_chunk_size_map)).elements()
