from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class YamlParser(object):
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        with open(self.filename, 'r') as stream:
            return load(stream, Loader=Loader)

    def dump(self, data):
        with open(self.filename, 'w') as stream:
            stream.write(dump(data, Dumper=Dumper))
