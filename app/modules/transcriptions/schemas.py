from marshmallow import Schema, fields

class TimestampSchema(Schema):
    t = fields.Float(required=True)
    w = fields.String(required=True)

class TranscriptionSchema(Schema):
    _id = fields.Integer(dump_only=True)
    audioId = fields.Integer(required=True)
    text = fields.String(required=True)
    timestamps = fields.List(fields.Nested(TimestampSchema), load_default=[])
    created_at = fields.DateTime(dump_only=True)
