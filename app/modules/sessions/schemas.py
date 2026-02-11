from marshmallow import Schema, fields

class SessionSchema(Schema):
    _id = fields.Integer(dump_only=True)
    userId = fields.Integer(required=True)
    tokenJwt = fields.String(required=True)
    startedAt = fields.DateTime(dump_only=True)
    expiresAt = fields.DateTime(required=True)
