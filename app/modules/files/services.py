from bson import ObjectId
from app.core.base_service import BaseService

class FileService(BaseService):
    collection_name = "files"
    # id_type = int

    @classmethod
    def create(cls, data):
        if 'userId' in data:
            data['userId'] = ObjectId(data['userId'])
        if 'folderId' in data:
            data['folderId'] = ObjectId(data['folderId'])
        if 'tagIds' in data and data['tagIds']:
            data['tagIds'] = [ObjectId(tag_id) for tag_id in data['tagIds']]
        return super().create(data)
