from datetime import datetime

class Tag:
    def __init__(self, name):
        self.name = name
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "name": self.name,
            "createdAt": self.createdAt
        }
