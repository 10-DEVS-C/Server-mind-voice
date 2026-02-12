from datetime import datetime

class AiAnalysis:
    def __init__(self, transcriptionId, result):
        self.transcriptionId = transcriptionId
        self.result = result
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "transcriptionId": self.transcriptionId,
            "result": self.result,
            "createdAt": self.createdAt
        }
