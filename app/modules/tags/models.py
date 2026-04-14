from datetime import datetime

class Tag:
    def __init__(self, name, user_id=None):
        self.name = name
        self.userId = user_id
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "name": self.name,
            "userId": self.userId,
            "createdAt": self.createdAt
        }
