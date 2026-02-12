from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class ActivityLogSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=True, validate=validate_object_id)
    action = fields.String(required=True)
    ip = fields.String(required=True)
    createdAt = fields.DateTime(dump_only=True)
