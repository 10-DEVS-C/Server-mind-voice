from datetime import datetime

class Role:
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions
        self.permissions = permissions
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "name": self.name,
            "permissions": self.permissions,
            "createdAt": self.createdAt
        }
