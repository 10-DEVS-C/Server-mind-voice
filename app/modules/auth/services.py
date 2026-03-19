from flask_jwt_extended import create_access_token
from app.modules.users.services import UserService
from app.modules.users.models import User
from app.modules.roles.services import RoleService

class AuthService:
    @staticmethod
    def login(data):
        username = data.get('username')
        password = data.get('password')
        
        user_data = UserService.get_by_username(username)
        if not user_data:
            return None
            
        # user_data is a dict from mongodb, we need to verify password
        # stored password hash is in user_data['passwordHash']
        if User.verify_password(user_data['passwordHash'], password):
            role_name = "user"
            if user_data.get('roleId'):
                role_data = RoleService.get_by_id(user_data['roleId'])
                if role_data:
                    role_name = role_data.get('name', 'user').lower()

            additional_claims = {
                "name": user_data.get("name"),
                "role": role_name
            }
            access_token = create_access_token(identity=str(user_data['_id']), additional_claims=additional_claims)
            return access_token
        
        return None
