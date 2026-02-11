from marshmallow import Schema, fields

class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

class TokenSchema(Schema):
    access_token = fields.String(required=True)
