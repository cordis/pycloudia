from inspect import getmembers
from itertools import imap, ifilter
from operator import itemgetter
from zope.interface import Interface, implements

from pycloudia.channels.declarative import ChannelDeclaration


class InvokerReaderInterface(Interface):
    def get_channels():
        pass


class InvokerReader(object):
    implements(InvokerReaderInterface)

    def __init__(self, invoker):
        self.invoker = invoker

    def get_channels(self):
        members = imap(itemgetter('1'), getmembers(self.invoker))
        return ifilter(self._is_channel_method, members)

    def _is_channel_method(self, member):
        return isinstance(member, ChannelDeclaration)
