from marshmallow import Schema, fields

from app.core.validations import validate_object_id

class PreferencesSchema(Schema):
    theme = fields.String(load_default="light")
    language = fields.String(load_default="es")
    notifications = fields.Boolean(load_default=True)

class ProfileSchema(Schema):
    _id = fields.String(dump_only=True)
    userId = fields.String(required=True, validate=validate_object_id)
    photo = fields.String()
    preferences = fields.Nested(PreferencesSchema)
    updatedAt = fields.DateTime(dump_only=True)
