from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import AudioSchema
from .services import AudioService
from app.core.auth_utils import is_admin, get_current_user_id, check_ownership

blp = Blueprint("audios", __name__, description="Operations on audios")

@blp.route("/")
class AudioList(MethodView):
    @blp.response(200, AudioSchema(many=True))
    @jwt_required()
    def get(self):
        """List all audios"""
        query = {} if is_admin() else {"userId": ObjectId(get_current_user_id())}
        return AudioService.get_all(query)

    @blp.arguments(AudioSchema)
    @blp.response(201, AudioSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new audio record"""
        if not is_admin() or 'userId' not in new_data:
            new_data['userId'] = get_current_user_id()
        audio_id = AudioService.create(new_data)
        return AudioService.get_by_id(audio_id)

@blp.route("/<string:audio_id>")
class AudioResource(MethodView):
    @blp.response(200, AudioSchema)
    @jwt_required()
    def get(self, audio_id):
        """Get audio by ID"""
        audio = AudioService.get_by_id(audio_id)
        if not audio:
            abort(404, message="Audio not found")
        check_ownership(audio)
        return audio

    @blp.response(204)
    @jwt_required()
    def delete(self, audio_id):
        """Delete audio"""
        audio = AudioService.get_by_id(audio_id)
        if not audio:
            abort(404, message="Audio not found")
        check_ownership(audio)

        if not AudioService.delete(audio_id):
            abort(404, message="Audio not found")
        return ""
