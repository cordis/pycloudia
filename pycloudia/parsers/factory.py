from os import path

from pycloudia.parsers.yaml_parser import YamlParser


class ParserNotFound(RuntimeError):
    pass


class ParserFactory(object):
    extension_to_parser_cls = {
        'yaml': YamlParser,
    }

    def __call__(self, filename):
        _, extension = path.splitext(filename)
        try:
            return self.extension_to_parser_cls[extension.lower()](filename)
        except KeyError:
            raise ParserNotFound(extension.lower())
