from app.core.base_service import BaseService
from .models import User

class UserService(BaseService):
    collection_name = "users"
    id_type = int

    @classmethod
    def create_user(cls, data):
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role_id=data.get('roleId', 2) # Default role ID 2 (Usuario)
        )
        return cls.create(user.to_dict())

    @classmethod
    def get_by_username(cls, username):
        return cls.get_collection().find_one({"username": username})
