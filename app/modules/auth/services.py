from flask_jwt_extended import create_access_token
from app.modules.users.services import UserService
from app.modules.users.models import User

class AuthService:
    @staticmethod
    def login(data):
        username = data.get('username')
        password = data.get('password')
        
        user_data = UserService.get_by_username(username)
        if not user_data:
            return None
            
        # user_data is a dict from mongodb, we need to verify password
        # stored password hash is in user_data['password_hash']
        if User.verify_password(user_data['password_hash'], password):
            access_token = create_access_token(identity=str(user_data['_id']))
            return access_token
        
        return None
