from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class DocumentSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=True, validate=validate_object_id)
    folderId = fields.String(required=True, validate=validate_object_id)
    title = fields.String(required=True)
    type = fields.String(load_default="nota")
    content = fields.Dict(load_default={})
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)
