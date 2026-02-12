from datetime import datetime

class Session:
    def __init__(self, user_id, token_jwt, expires_at):
        self.user_id = user_id
        self.token_jwt = token_jwt
        self.token_jwt = token_jwt
        self.startedAt = datetime.utcnow()
        self.expiresAt = expires_at

    def to_dict(self):
        return {
            "userId": self.user_id,
            "tokenJwt": self.token_jwt,
            "startedAt": self.startedAt,
            "expiresAt": self.expiresAt
        }
