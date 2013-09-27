from pyschema import Schema, List, Builder, Str, Dict, Node, Int


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


class InitRequestSchema(Schema):
    internal_host = Str()
    external_host = Str()


class InitResponseSchema(Schema):
    worker_id = Str()


class OldInitResponseSchema(Schema):
    services = List(Builder(ServiceSchema))
    channels = List(Builder(ChannelSchema))


class MachineSchema(Schema):
    name = Str()
    host = Str()


class ClusterSchema(Schema):
    name = Str()
    machines = List(Builder(MachineSchema))


class ConfigSchema(Schema):
    machine = Str()
    port = Int()


class ClustersConfigSchema(Schema):
    clusters = List(Builder(ClusterSchema))
    configs = List(Builder(ConfigSchema))


class ChannelsConfigSchema(Schema):
    defaults = Dict(Str())
    channels = Dict(Dict(Str()))
