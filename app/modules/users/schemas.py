from marshmallow import Schema, fields

class UserSchema(Schema):
    _id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    status = fields.String()
    roleId = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class UserCreateSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    roleId = fields.Integer(load_default=2) # Default to User role

class UserUpdateSchema(Schema):
    username = fields.String()
    email = fields.Email()
    password = fields.String(load_only=True)
    status = fields.String()
    roleId = fields.Integer()

class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
