from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from .services import UserService
from app.core.utils import ApiResponse
from app.core.auth_utils import is_admin, get_current_user_id

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    @jwt_required()
    def get(self):
        """List all users"""
        if not is_admin():
             # Non admins only get themselves
             users = [UserService.get_by_id(get_current_user_id())]
             return [u for u in users if u]
        users = UserService.get_all()
        return users

    @blp.arguments(UserCreateSchema)
    @blp.response(201, UserSchema)
    def post(self, new_data):
        """Create a new user"""
        if UserService.get_by_username(new_data['username']):
            abort(409, message="Username already exists")
        
        user_id = UserService.create_user(new_data)
        user = UserService.get_by_id(user_id)
        return user

@blp.route("/<string:user_id>")
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    @jwt_required()
    def get(self, user_id):
        """Get user by ID"""
        if not is_admin() and str(user_id) != str(get_current_user_id()):
             abort(403, message="You can only access your own data")
             
        user = UserService.get_by_id(user_id)
        if not user:
            abort(404, message="User not found")
        return user

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    @jwt_required()
    def put(self, update_data, user_id):
        """Update existing user"""
        if not is_admin() and str(user_id) != str(get_current_user_id()):
             abort(403, message="You can only access your own data")

        if not UserService.update(user_id, update_data):
            abort(404, message="User not found or update failed")
        return UserService.get_by_id(user_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, user_id):
        """Delete user"""
        if not is_admin() and str(user_id) != str(get_current_user_id()):
             abort(403, message="You can only access your own data")

        if not UserService.delete(user_id):
            abort(404, message="User not found")
        return ""
