from pycloudia.channels.address import AddressSchema
from pyschema import *


class ConfigSubscriptionSchema(Schema):
    channel_name = Str()
    address_list = List(Builder(AddressSchema()))
