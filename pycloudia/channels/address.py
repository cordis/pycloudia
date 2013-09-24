from pyschema import *


class Address(object):
    host = None
    port = None

    @classmethod
    def from_string(cls, address_string):
        host, port = address_string.split(':')
        instance = cls()
        instance.host = host
        instance.port = int(port)
        return instance


class AddressSchema(Schema):
    Object = Address

    host = Str()
    port = Int()
