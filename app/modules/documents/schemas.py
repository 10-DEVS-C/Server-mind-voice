from marshmallow import Schema, fields

class DocumentSchema(Schema):
    _id = fields.Integer(dump_only=True)
    userId = fields.Integer(required=True)
    folderId = fields.Integer(required=True)
    title = fields.String(required=True)
    type = fields.String(load_default="nota")
    content = fields.Dict(load_default={})
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
