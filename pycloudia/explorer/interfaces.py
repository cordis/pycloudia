from zope.interface import Interface, Attribute


class IAgentConfig(Interface):
    host = Attribute('host', ':type: C{str}')
    min_port = Attribute('min_port', ':type: C{int}')
    max_port = Attribute('max_port', ':type: C{int}')
    identity = Attribute('identity', ':type: C{str}')
