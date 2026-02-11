from marshmallow import Schema, fields

class PreferencesSchema(Schema):
    theme = fields.String(load_default="light")
    language = fields.String(load_default="es")
    notifications = fields.Boolean(load_default=True)

class ProfileSchema(Schema):
    _id = fields.Integer(dump_only=True)
    userId = fields.Integer(required=True)
    photo = fields.String()
    preferences = fields.Nested(PreferencesSchema)
    updated_at = fields.DateTime(dump_only=True)
