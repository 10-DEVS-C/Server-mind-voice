from datetime import datetime

class Role:
    def __init__(self, name, permissions):
        self.name = name
        self.permissions = permissions
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "name": self.name,
            "permissions": self.permissions,
            "created_at": self.created_at
        }
