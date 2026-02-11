from marshmallow import Schema, fields

class FileSchema(Schema):
    _id = fields.Integer(dump_only=True)
    userId = fields.Integer(required=True)
    folderId = fields.Integer(required=True)
    title = fields.String(required=True)
    type = fields.String(load_default="txt")
    tagIds = fields.List(fields.Integer(), load_default=[])
    deleted = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
