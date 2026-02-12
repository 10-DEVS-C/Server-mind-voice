from bson import ObjectId
from app.core.base_service import BaseService

class FolderService(BaseService):
    collection_name = "folders"
    # id_type = int

    @classmethod
    def get_all_by_user(cls, user_id):
        return cls.get_collection().find({"userId": ObjectId(user_id)})

    @classmethod
    def create(cls, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        if data.get('parentFolderId'):
            data['parentFolderId'] = ObjectId(data['parentFolderId'])
        return super().create(data)
