from datetime import datetime

class Profile:
    def __init__(self, user_id, photo=None, preferences=None):
        self.user_id = user_id
        self.photo = photo
        self.preferences = preferences or {
            "theme": "light",
            "language": "es",
            "notifications": True
        }
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.user_id,
            "photo": self.photo,
            "preferences": self.preferences,
            "updated_at": self.updated_at
        }
