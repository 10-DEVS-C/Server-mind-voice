from marshmallow import Schema, fields
from app.core.validations import validate_object_id

class AiAnalysisSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(dump_only=True)
    transcriptionId = fields.String(required=False, allow_none=True, validate=validate_object_id)
    result = fields.Dict(required=True)
    createdAt = fields.DateTime(dump_only=True)
