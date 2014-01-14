class SERVICE(object):
    NAME = 'gateways'


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
    AUTH_PLATFORM = 'X-Clients-Auth-Platform'
    AUTH_ACCESS_TOKEN = 'X-Clients-Auth-Access-Token'
