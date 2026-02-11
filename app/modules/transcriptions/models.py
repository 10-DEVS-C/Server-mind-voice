from datetime import datetime

class Transcription:
    def __init__(self, audio_id, text, timestamps=None):
        self.audio_id = audio_id
        self.text = text
        self.timestamps = timestamps or []
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "audioId": self.audio_id,
            "text": self.text,
            "timestamps": self.timestamps,
            "created_at": self.created_at
        }
