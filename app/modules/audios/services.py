from bson import ObjectId
from app.core.base_service import BaseService

class AudioService(BaseService):
    collection_name = "audios"
    # id_type = int

    @classmethod
    def create(cls, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        return super().create(data)
