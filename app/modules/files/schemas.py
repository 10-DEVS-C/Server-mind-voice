from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class FileSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=True, validate=validate_object_id)
    folderId = fields.String(required=True, validate=validate_object_id)
    title = fields.String(required=True)
    type = fields.String(load_default="txt")
    tagIds = fields.List(fields.String(validate=validate_object_id), load_default=[])
    deleted = fields.Boolean(dump_only=True)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
