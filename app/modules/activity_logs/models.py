from datetime import datetime

class ActivityLog:
    def __init__(self, userId, action, ip):
        self.userId = userId
        self.action = action
        self.ip = ip
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.userId,
            "action": self.action,
            "ip": self.ip,
            "createdAt": self.createdAt
        }
