from pyschema import Schema, List, Builder, Str, Dict, Node


class PullSchema(Schema):
    channel = Str()
    handle = Str()


class PushSchema(Schema):
    channel = Str()
    method = Str()
    broadcast = Str()


class ServiceSchema(Schema):
    name = Str()
    identity = Str()
    factory = Dict(Node())
    options = Dict(Node())
    pull = Dict(Builder(PullSchema), Str())
    push = Dict(Builder(PushSchema), Str())


class ChannelSchema(Schema):
    name = Str()
    port = Str()


class InitResponseSchema(Schema):
    services = List(Builder(ServiceSchema))
    channels = List(Builder(ChannelSchema))
