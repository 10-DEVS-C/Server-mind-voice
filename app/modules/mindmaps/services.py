from bson import ObjectId
from app.core.base_service import BaseService

class MindmapService(BaseService):
    collection_name = "mindmaps"
    # id_type = int

    @classmethod
    def create(cls, data):
        if 'documentId' in data:
            data['documentId'] = ObjectId(data['documentId'])
        return super().create(data)
