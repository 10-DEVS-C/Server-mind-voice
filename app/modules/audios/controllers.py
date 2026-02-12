from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import AudioSchema
from .services import AudioService

blp = Blueprint("audios", __name__, description="Operations on audios")

@blp.route("/")
class AudioList(MethodView):
    @blp.response(200, AudioSchema(many=True))
    @jwt_required()
    def get(self):
        """List all audios"""
        return AudioService.get_all()

    @blp.arguments(AudioSchema)
    @blp.response(201, AudioSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new audio record"""
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
        return audio

    @blp.response(204)
    @jwt_required()
    def delete(self, audio_id):
        """Delete audio"""
        if not AudioService.delete(audio_id):
            abort(404, message="Audio not found")
        return ""
