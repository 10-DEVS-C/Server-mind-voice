from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    def __init__(self, username, email, password, role_id, name=None, status="active"):
        self.username = username
        self.email = email
        self.passwordHash = generate_password_hash(password)
        self.name = name
        self.status = status
        self.role_id = role_id
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "passwordHash": self.passwordHash,
            "name": self.name,
            "status": self.status,
            "roleId": self.role_id,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

    @staticmethod
    def verify_password(passwordHash, password):
        return check_password_hash(passwordHash, password)
