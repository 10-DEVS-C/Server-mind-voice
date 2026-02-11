from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    def __init__(self, username, email, password, role_id, status="active"):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.status = status
        self.role_id = role_id
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "status": self.status,
            "roleId": self.role_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def verify_password(password_hash, password):
        return check_password_hash(password_hash, password)
