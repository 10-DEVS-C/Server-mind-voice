from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class UserSchema(Schema):
    _id = fields.String(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    name = fields.String()
    status = fields.String()
    roleId = fields.String(validate=validate_object_id)
    createdAt = fields.DateTime(dump_only=True)
    updatedAt = fields.DateTime(dump_only=True)

class UserCreateSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    name = fields.String(required=True)
    roleId = fields.String(load_default="661d4a0b2f4a8a001c9a1a1a", validate=validate_object_id) # Default User Role ID

class UserUpdateSchema(Schema):
    username = fields.String()
    email = fields.Email()
    password = fields.String(load_only=True)
    name = fields.String()
    status = fields.String()
    roleId = fields.String(validate=validate_object_id)

class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
