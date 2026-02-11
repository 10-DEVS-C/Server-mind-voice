from datetime import datetime

class Tag:
    def __init__(self, name):
        self.name = name
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "name": self.name,
            "created_at": self.created_at
        }
