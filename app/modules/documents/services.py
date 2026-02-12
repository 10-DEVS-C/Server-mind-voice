from bson import ObjectId
from app.core.base_service import BaseService

class DocumentService(BaseService):
    collection_name = "documents"
    # id_type = int

    @classmethod
    def create(cls, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        if 'folderId' in data:
            data['folderId'] = ObjectId(data['folderId'])
        return super().create(data)
