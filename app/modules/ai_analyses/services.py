from bson import ObjectId
from app.core.base_service import BaseService

class AiAnalysisService(BaseService):
    collection_name = "ai_analyses"
    # id_type = int

    @classmethod
    def create(cls, data):
        if 'transcriptionId' in data:
            data['transcriptionId'] = ObjectId(data['transcriptionId'])
        return super().create(data)
