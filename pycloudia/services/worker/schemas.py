from pyschema import *


class SubscriptionChannelSchema(Schema):
    name = Str()
    host = Str()
    port = Int()
    topic = Str()


class ConfigSubscriptionSchema(Schema):
    channels = List(Builder(SubscriptionChannelSchema()))
