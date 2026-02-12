from datetime import datetime

class Session:
    def __init__(self, userId, tokenJwt, expiresAt):
        self.userId = userId
        self.tokenJwt = tokenJwt
        self.startedAt = datetime.utcnow()
        self.expiresAt = expiresAt

    def to_dict(self):
        return {
            "userId": self.userId,
            "tokenJwt": self.tokenJwt,
            "startedAt": self.startedAt,
            "expiresAt": self.expiresAt
        }
