from pycloudia.packages.interfaces import IPackage


class Package(object, IPackage):
    def __init__(self, content, headers=None):
        self.content = content
        self.headers = headers or {}
