class SERVICE(object):
    NAME = 'gateways'


class COMMAND(object):
    CREATE = 'create'
    DELETE = 'delete'
    AUTHENTICATE = 'authorize'


class SOURCE(object):
    EXTERNAL = 'external'
    INTERNAL = 'internal'


class HEADER(object):
    SOURCE = 'X-Clients-Source'
    USER_ID = 'X-Clients-User-Id'
    SERVICE = 'X-Router-Service'
    COMMAND = 'X-Router-Command'
    CLIENT_ID = 'X-Clients-Client-Id'
    AUTH_PLATFORM = 'X-Clients-Auth-Platform'
    AUTH_ACCESS_TOKEN = 'X-Clients-Auth-Access-Token'
