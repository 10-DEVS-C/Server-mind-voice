from marshmallow import Schema, fields

class TagSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(allow_none=True, dump_only=True)
    name = fields.String(required=True)
    createdAt = fields.DateTime(dump_only=True)

class TagQueryArgsSchema(Schema):
    name = fields.String(required=False, metadata={"description": "Filtro dinámico de búsqueda parcial para el nombre del Tag"})
