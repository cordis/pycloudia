from zope.interface import implementer

from pycloudia.packages.interfaces import IPackage


@implementer(IPackage)
class Package(object):
    def __init__(self, content, headers=None):
        self.content = content
        self.headers = headers or {}
