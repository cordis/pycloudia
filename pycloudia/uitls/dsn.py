import sys
import urlparse
import re


class DsnParser(object):
    kwargs_re = re.compile('/(\w+)=([^/]+)')
    default_parts = ['scheme', 'hostname', 'username', 'password', 'port']
    params_map = {
        'scheme': (str, 'scheme'),
        'username': (str, 'user'),
        'password': (str, 'pass'),
        'hostname': (str, 'host'),
        'port': (int, 'port'),
        'kwargs': {},
    }

    def __init__(self, params_map=None):
        if params_map is not None:
            self.params_map.update(params_map)

    def parse(self, dsn):
        parts = urlparse.urlparse(dsn)
        config = {}
        config = self._parse_default_parts(config, parts)
        config = self._parse_kwargs(config, parts)
        return config

    def _parse_default_parts(self, config, parts):
        for part in self.default_parts:
            if not getattr(parts, part):
                continue
            factory, key = self.params_map[part]
            config[key] = factory(getattr(parts, part))
        return config

    def _parse_kwargs(self, config, parts):
        config['kwargs'] = {}
        for match in self.kwargs_re(parts.path):
            key = match.group(1)
            if key not in self.params_map['kwargs']:
                continue
            factory, key = self.params_map['kwargs']['key']
            config['kwargs'][key] = factory(match.group(2))
        return config


def test():
    if len(sys.argv) < 2:
        sys.exit('Usage: python %s "myScheme://username:password@hostname:12345/kwarg1=1/kwarg2=2"' % sys.argv[0])

    config = DsnParser({
        'kwargs': {
            'kwarg1': (int, 'kw1'),
            'kwarg2': (str, 'kw2'),
        }
    }).parse(sys.argv[1])
    assert config == {
        'scheme': 'myScheme',
        'username': 'username',
        'password': 'password',
        'hostname': 'hostname',
        'port': 12345,
        'kwargs': {
            'kw1': 1,
            'kw2': '2'
        }
    }


if __name__ == "__main__":
    test()
