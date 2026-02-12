from datetime import datetime

class Audio:
    def __init__(self, userId, filePath, duration, audioFormat="wav"):
        self.userId = userId
        self.filePath = filePath
        self.duration = duration
        self.format = audioFormat
        self.recordedAt = datetime.utcnow()
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.userId,
            "filePath": self.filePath,
            "duration": self.duration,
            "format": self.format,
            "recordedAt": self.recordedAt,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
