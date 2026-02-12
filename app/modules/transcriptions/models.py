from datetime import datetime

class Transcription:
    def __init__(self, audioId, text, timestamps=None):
        self.audioId = audioId
        self.text = text
        self.timestamps = timestamps or []
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "audioId": self.audioId,
            "text": self.text,
            "timestamps": self.timestamps,
            "createdAt": self.createdAt
        }
