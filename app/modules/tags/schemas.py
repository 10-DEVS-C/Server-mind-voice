from marshmallow import Schema, fields

class TagSchema(Schema):
    _id = fields.String(dump_only=True)
    name = fields.String(required=True)
    createdAt = fields.DateTime(dump_only=True)
