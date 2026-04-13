from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class FolderSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=False, validate=validate_object_id)
    name = fields.String(required=True)
    parentFolderId = fields.String(allow_none=True, load_default=None, validate=validate_object_id)
    createdAt = fields.DateTime(dump_only=True)

class FolderQueryArgsSchema(Schema):
    name = fields.String(required=False, metadata={"description": "Filtro dinámico de búsqueda parcial para el nombre (Regex inteligente)"})
