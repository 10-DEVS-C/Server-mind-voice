from datetime import datetime

class Audio:
    def __init__(self, user_id, file_path, duration, audio_format="wav"):
        self.user_id = user_id
        self.file_path = file_path
        self.duration = duration
        self.format = audio_format
        self.recorded_at = datetime.utcnow()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.user_id,
            "filePath": self.file_path,
            "duration": self.duration,
            "format": self.format,
            "recordedAt": self.recorded_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
