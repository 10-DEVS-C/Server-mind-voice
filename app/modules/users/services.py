from bson import ObjectId
from app.core.base_service import BaseService
from .models import User
from werkzeug.security import generate_password_hash

class UserService(BaseService):
    collection_name = "users"
    # id_type = int

    @classmethod
    def create_user(cls, data):
        roleId = data.get('roleId')
        if roleId:
            roleId = ObjectId(roleId)

        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            name=data.get('name'),
            roleId=roleId
        )
        return cls.create(user.to_dict())

    @classmethod
    def get_by_username(cls, username):
        return cls.get_collection().find_one({"username": username})

    @classmethod
    def update(cls, item_id, data):
        # Hash password if present
        if 'password' in data:
            data['passwordHash'] = generate_password_hash(data.pop('password'))
            
        # Convert roleId to ObjectId if present
        if 'roleId' in data and data['roleId']:
            data['roleId'] = ObjectId(data.pop('roleId'))
        
        # Remove fields that should not be updated or are None (if partial update desired)
        # Marshmallow should handle validation, but we can clean up here
        data = {k: v for k, v in data.items() if v is not None}
        
        return super().update(item_id, data)
