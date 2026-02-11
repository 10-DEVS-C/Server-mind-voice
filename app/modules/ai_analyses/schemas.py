from marshmallow import Schema, fields

class ActionSchema(Schema):
    accion = fields.String(required=True)
    prioridad = fields.String(required=True)

class AnalysisResultSchema(Schema):
    resumen = fields.String(required=True)
    temas = fields.List(fields.String(), load_default=[])
    acciones = fields.List(fields.Nested(ActionSchema), load_default=[])
    sentimiento = fields.String()

class AiAnalysisSchema(Schema):
    _id = fields.Integer(dump_only=True)
    transcriptionId = fields.Integer(required=True)
    result = fields.Nested(AnalysisResultSchema, required=True)
    created_at = fields.DateTime(dump_only=True)
