from bson import ObjectId
from app.core.base_service import BaseService
from datetime import datetime

class AudioService(BaseService):
    collection_name = "audios"
    # id_type = int

    @classmethod
    def create(cls, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        now = datetime.utcnow()
        data.setdefault('recordedAt', now)
        data.setdefault('createdAt', now)
        data['updatedAt'] = now
        return super().create(data)

    @classmethod
    def update(cls, item_id, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        data['updatedAt'] = datetime.utcnow()
        return super().update(item_id, data)
