from flask.views import MethodView
from flask_smorest import Blueprint, abort
from .schemas import LoginSchema, TokenSchema
from .services import AuthService

blp = Blueprint("auth", __name__, description="Authentication operations")

@blp.route("/login")
class Login(MethodView):
    @blp.arguments(LoginSchema)
    @blp.response(200, TokenSchema)
    def post(self, login_data):
        """User Login"""
        access_token = AuthService.login(login_data)
        if not access_token:
            abort(401, message="Invalid username or password")
        
        return {"access_token": access_token}
