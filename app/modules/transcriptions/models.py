from datetime import datetime

class Transcription:
    def __init__(self, audio_id, text, timestamps=None):
        self.audio_id = audio_id
        self.text = text
        self.timestamps = timestamps or []
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "audioId": self.audio_id,
            "text": self.text,
            "timestamps": self.timestamps,
            "createdAt": self.createdAt
        }
