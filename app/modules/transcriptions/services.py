from bson import ObjectId
from app.core.base_service import BaseService

class TranscriptionService(BaseService):
    collection_name = "transcriptions"
    # id_type = int

    @classmethod
    def create(cls, data):
        if 'audioId' in data:
            data['audioId'] = ObjectId(data['audioId'])
        return super().create(data)
