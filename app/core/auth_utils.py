from functools import wraps
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_smorest import abort

def require_role(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role", "").lower() != role_name.lower():
                abort(403, message=f"Admin privileges required")
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user_id():
    return get_jwt_identity()

def is_admin():
    claims = get_jwt()
    return claims.get("role", "").lower() == "admin"

def check_ownership(resource):
    """
    Checks if the current user owns the resource or is an admin.
    The resource param must be a dict-like object containing 'userId'.
    """
    if not resource:
        abort(404, message="Resource not found")
        
    if is_admin():
        return True
        
    current_user_id = get_current_user_id()
    if str(resource.get('userId')) != str(current_user_id):
        abort(403, message="You do not have permission to access or modify this resource")
    return True
