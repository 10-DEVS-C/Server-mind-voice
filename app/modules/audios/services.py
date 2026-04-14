from bson import ObjectId
from app.core.base_service import BaseService
from datetime import datetime

class AudioService(BaseService):
    collection_name = "audios"
    # id_type = int

    @staticmethod
    def _normalize_relations(data):
        if 'folderId' in data:
            folder_id = data.get('folderId')
            data['folderId'] = ObjectId(folder_id) if folder_id else None

        if 'tagIds' in data:
            tag_ids = data.get('tagIds') or []
            data['tagIds'] = [ObjectId(tag_id) for tag_id in tag_ids]

    @classmethod
    def create(cls, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        cls._normalize_relations(data)
        now = datetime.utcnow()
        data.setdefault('recordedAt', now)
        data.setdefault('createdAt', now)
        data['updatedAt'] = now
        return super().create(data)

    @classmethod
    def update(cls, item_id, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        cls._normalize_relations(data)
        data['updatedAt'] = datetime.utcnow()
        return super().update(item_id, data)
