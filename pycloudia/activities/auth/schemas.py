from pyschema import Schema, Str


class RequestAuthenticateSchema(Schema):
    client_id = Str()
    platform = Str()
    access_token = Str()
