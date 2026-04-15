from marshmallow import ValidationError
from bson import ObjectId

def validate_object_id(value):
    """
    Validates that a string is a valid MongoDB ObjectId.
    Skips validation for None (paired fields use allow_none=True).
    """
    if value is None:
        return
    if not ObjectId.is_valid(value):
        raise ValidationError("Invalid ObjectId format.")
