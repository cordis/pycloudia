class SERVICE(object):
    NAME = 'clients'


class COMMAND(object):
    AUTHENTICATE = 'authorize'
    CREATE = 'create'
    DELETE = 'delete'


class SOURCE(object):
    EXTERNAL = 'external'
    INTERNAL = 'internal'


class HEADER(object):
    SOURCE = 'X-Clients-Source'
    USER_ID = 'X-Clients-User-Id'
    SERVICE = 'X-Clients-Service'
    COMMAND = 'X-Clients-Command'
    CLIENT_ID = 'X-Clients-Client-Id'
