from marshmallow import Schema, fields

class AudioSchema(Schema):
    _id = fields.Integer(dump_only=True)
    userId = fields.Integer(required=True)
    filePath = fields.String(required=True)
    duration = fields.Integer(required=True)
    format = fields.String(load_default="wav")
    recordedAt = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
