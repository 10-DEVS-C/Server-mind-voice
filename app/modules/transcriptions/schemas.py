from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class TimestampSchema(Schema):
    t = fields.Float(required=True)
    w = fields.String(required=True)

class TranscriptionSchema(Schema):
    _id = fields.String(dump_only=True)
    audioId = fields.String(required=True, validate=validate_object_id)
    text = fields.String(required=True)
    timestamps = fields.List(fields.Nested(TimestampSchema), load_default=[])
    createdAt = fields.DateTime(dump_only=True)
