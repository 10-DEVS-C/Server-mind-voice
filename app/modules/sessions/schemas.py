from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class SessionSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=True, validate=validate_object_id)
    tokenJwt = fields.String(required=True)
    startedAt = fields.DateTime(dump_only=True)
    expiresAt = fields.DateTime(required=True)
