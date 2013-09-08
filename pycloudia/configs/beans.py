from pyschema import Schema, List, Str, Builder, Int, Dict


class Machine(Schema):
    name = Str()
    host = Str()


class Config(Schema):
    machine = Builder(Machine)
    port = Int()


class Service(Schema):
    id = Str()
    name = Str()
    factory = Dict(Str())


class Channel(Schema):
    name = Str()
    port = Int()


class Node(Schema):
    machine = Builder(Machine)
    port = Int()
    services = List(Builder(Service))
    channels = List(Builder(Channel))


class Cluster(Schema):
    machines = List(Builder(Machine))
