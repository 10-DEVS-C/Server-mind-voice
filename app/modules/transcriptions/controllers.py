from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import TranscriptionSchema
from .services import TranscriptionService

blp = Blueprint("transcriptions", __name__, description="Operations on transcriptions")

@blp.route("/")
class TranscriptionList(MethodView):
    @blp.response(200, TranscriptionSchema(many=True))
    @jwt_required()
    def get(self):
        """List all transcriptions"""
        return TranscriptionService.get_all()

    @blp.arguments(TranscriptionSchema)
    @blp.response(201, TranscriptionSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new transcription"""
        transcription_id = TranscriptionService.create(new_data)
        return TranscriptionService.get_by_id(transcription_id)

@blp.route("/<int:transcription_id>")
class TranscriptionResource(MethodView):
    @blp.response(200, TranscriptionSchema)
    @jwt_required()
    def get(self, transcription_id):
        """Get transcription by ID"""
        transcription = TranscriptionService.get_by_id(transcription_id)
        if not transcription:
            abort(404, message="Transcription not found")
        return transcription

    @blp.response(204)
    @jwt_required()
    def delete(self, transcription_id):
        """Delete transcription"""
        if not TranscriptionService.delete(transcription_id):
            abort(404, message="Transcription not found")
        return ""
