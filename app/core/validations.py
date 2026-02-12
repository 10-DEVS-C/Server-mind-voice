from marshmallow import ValidationError
from bson import ObjectId

def validate_object_id(value):
    """
    Validates that a string is a valid MongoDB ObjectId.
    """
    if not ObjectId.is_valid(value):
        raise ValidationError("Invalid ObjectId format.")
