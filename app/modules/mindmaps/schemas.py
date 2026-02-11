from marshmallow import Schema, fields

class MindmapSchema(Schema):
    _id = fields.Integer(dump_only=True)
    documentId = fields.Integer(required=True)
    nodes = fields.Dict(load_default={})
    updated_at = fields.DateTime(dump_only=True)
