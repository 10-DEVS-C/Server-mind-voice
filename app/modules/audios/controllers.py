from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from flask import current_app, request
from bson import ObjectId
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
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

@blp.route("/upload")
class AudioUpload(MethodView):
    @blp.response(201, AudioSchema)
    @jwt_required()
    def post(self):
        """Upload an audio file and create its record"""
        audio_file = request.files.get("file")
        if not audio_file or not audio_file.filename:
            abort(400, message="Audio file is required")

        duration = request.form.get("duration")
        if duration is None:
            abort(400, message="Duration is required")

        title = request.form.get("title") or audio_file.filename
        transcription = request.form.get("transcription")
        extension = os.path.splitext(secure_filename(audio_file.filename))[1] or ".m4a"

        audio_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "audios")
        os.makedirs(audio_dir, exist_ok=True)

        filename = f"{uuid4().hex}{extension}"
        absolute_path = os.path.join(audio_dir, filename)
        audio_file.save(absolute_path)

        relative_path = f"audios/{filename}"
        audio_id = AudioService.create({
            "userId": get_current_user_id(),
            "title": title,
            "filePath": relative_path,
            "duration": int(duration),
            "format": extension.replace(".", "") or "m4a",
            "transcription": transcription,
        })
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

    @blp.arguments(AudioSchema(partial=True))
    @blp.response(200, AudioSchema)
    @jwt_required()
    def put(self, update_data, audio_id):
        """Update audio metadata"""
        audio = AudioService.get_by_id(audio_id)
        if not audio:
            abort(404, message="Audio not found")
        check_ownership(audio)

        update_data.pop('userId', None)
        update_data.pop('filePath', None)

        if not AudioService.update(audio_id, update_data):
            abort(404, message="Audio not found")
        return AudioService.get_by_id(audio_id)

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
