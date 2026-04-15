from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class AnalyzeTextSchema(Schema):
    text = fields.String(required=False, metadata={"description": "El texto extraído para ser procesado. Opcional si se envía transcriptionId"})
    transcriptionId = fields.String(required=False, allow_none=True, validate=validate_object_id, metadata={"description": "Id opcional de una transcripción existente"})
    api_key = fields.String(required=False, metadata={"description": "Opcional. API Key de Gemini a usar."})

class ExtractTextResponseSchema(Schema):
    extracted_text = fields.String(metadata={"description": "El texto extraído del archivo."})
