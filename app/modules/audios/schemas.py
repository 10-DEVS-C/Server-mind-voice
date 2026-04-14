from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class AudioSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=True, validate=validate_object_id)
    title = fields.String(load_default="Audio")
    filePath = fields.String(required=True)
    duration = fields.Integer(required=True)
    format = fields.String(load_default="wav")
    transcription = fields.String(allow_none=True, load_default=None)
    folderId = fields.String(allow_none=True, load_default=None, validate=validate_object_id)
    tagIds = fields.List(fields.String(validate=validate_object_id), load_default=[])
    recordedAt = fields.DateTime(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
