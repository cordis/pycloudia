from zope.interface import Interface, Attribute


class IAgentConfig(Interface):
    host = Attribute(''':type: C{str}''')
    min_port = Attribute(''':type: C{int}''')
    max_port = Attribute(''':type: C{int}''')
    identity = Attribute(''':type: C{str}''')
