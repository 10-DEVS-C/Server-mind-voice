from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class ActionSchema(Schema):
    accion = fields.String(required=True)
    prioridad = fields.String(required=True)

class AnalysisResultSchema(Schema):
    resumen = fields.String(required=True)
    temas = fields.List(fields.String(), load_default=[])
    acciones = fields.List(fields.Nested(ActionSchema), load_default=[])
    sentimiento = fields.String()

class AiAnalysisSchema(Schema):
    _id = fields.String(dump_only=True)
    transcriptionId = fields.String(required=True, validate=validate_object_id)
    result = fields.Nested(AnalysisResultSchema, required=True)
    createdAt = fields.DateTime(dump_only=True)
