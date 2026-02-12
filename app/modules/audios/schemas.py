from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class AudioSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=True, validate=validate_object_id)
    filePath = fields.String(required=True)
    duration = fields.Integer(required=True)
    format = fields.String(load_default="wav")
    recordedAt = fields.DateTime(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
