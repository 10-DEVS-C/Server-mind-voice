from datetime import datetime

class ActivityLog:
    def __init__(self, user_id, action, ip):
        self.user_id = user_id
        self.action = action
        self.ip = ip
        self.action = action
        self.ip = ip
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.user_id,
            "action": self.action,
            "ip": self.ip,
            "createdAt": self.createdAt
        }
