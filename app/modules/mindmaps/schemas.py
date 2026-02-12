from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class MindmapSchema(Schema):
    _id = fields.String(dump_only=True)
    documentId = fields.String(required=True, validate=validate_object_id)
    nodes = fields.Dict(load_default={})
    updatedAt = fields.DateTime(dump_only=True)
