class ACTIVITY(object):
    NAME = 'clients'


class COMMAND(object):
    CREATE = 'create'
    DELETE = 'delete'


class SOURCE(object):
    EXTERNAL = 'external'
    INTERNAL = 'internal'


class HEADER(object):
    SOURCE = 'X-Source'
    COMMAND = 'X-Command'
    CLIENT_ID = 'X-Client-Id'
