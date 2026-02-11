from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import ProfileSchema
from .services import ProfileService

blp = Blueprint("profiles", __name__, description="Operations on user profiles")

@blp.route("/")
class ProfileList(MethodView):
    @blp.response(200, ProfileSchema(many=True))
    @jwt_required()
    def get(self):
        """List all profiles"""
        return ProfileService.get_all()

    @blp.arguments(ProfileSchema)
    @blp.response(201, ProfileSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new profile"""
        # Ensure only one profile per user
        if ProfileService.get_by_user_id(new_data['userId']):
             abort(409, message="Profile already exists for this user")

        profile_id = ProfileService.create(new_data)
        return ProfileService.get_by_id(profile_id)

@blp.route("/<int:profile_id>")
class ProfileResource(MethodView):
    @blp.response(200, ProfileSchema)
    @jwt_required()
    def get(self, profile_id):
        """Get profile by ID"""
        profile = ProfileService.get_by_id(profile_id)
        if not profile:
            abort(404, message="Profile not found")
        return profile

    @blp.arguments(ProfileSchema)
    @blp.response(200, ProfileSchema)
    @jwt_required()
    def put(self, update_data, profile_id):
        """Update existing profile"""
        if not ProfileService.update(profile_id, update_data):
            abort(404, message="Profile not found")
        return ProfileService.get_by_id(profile_id)
