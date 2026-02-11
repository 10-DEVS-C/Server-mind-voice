from datetime import datetime

class AiAnalysis:
    def __init__(self, transcription_id, result):
        self.transcription_id = transcription_id
        self.result = result
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            "transcriptionId": self.transcription_id,
            "result": self.result,
            "created_at": self.created_at
        }
