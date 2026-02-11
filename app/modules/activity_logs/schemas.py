from marshmallow import Schema, fields

class ActivityLogSchema(Schema):
    _id = fields.Integer(dump_only=True)
    userId = fields.Integer(required=True)
    action = fields.String(required=True)
    ip = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
