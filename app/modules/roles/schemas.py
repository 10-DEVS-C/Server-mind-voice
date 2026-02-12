from marshmallow import Schema, fields

class RoleSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String(required=True)
    permissions = fields.Dict(keys=fields.String(), values=fields.Raw(), required=True)
    createdAt = fields.DateTime(dump_only=True)
