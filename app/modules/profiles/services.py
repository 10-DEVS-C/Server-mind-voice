from app.core.base_service import BaseService

class ProfileService(BaseService):
    collection_name = "profiles"
    id_type = int
    
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.get_collection().find_one({"userId": user_id})
