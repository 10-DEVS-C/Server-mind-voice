from marshmallow import Schema, fields

class FolderSchema(Schema):
    _id = fields.Integer(dump_only=True)
    userId = fields.Integer(required=True)
    name = fields.String(required=True)
    parentFolderId = fields.Integer(allow_none=True, load_default=None)
    created_at = fields.DateTime(dump_only=True)
