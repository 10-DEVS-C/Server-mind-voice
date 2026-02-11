from marshmallow import Schema, fields

class TagSchema(Schema):
    _id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
