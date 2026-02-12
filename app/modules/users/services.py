from bson import ObjectId
from app.core.base_service import BaseService
from .models import User

class UserService(BaseService):
    collection_name = "users"
    # id_type = int

    @classmethod
    def create_user(cls, data):
        print(f"DEBUG: create_user data: {data}")
        role_id = data.get('roleId')
        if role_id:
            role_id = ObjectId(role_id)

        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            name=data.get('name'),
            role_id=role_id
        )
        return cls.create(user.to_dict())

    @classmethod
    def get_by_username(cls, username):
        return cls.get_collection().find_one({"username": username})
