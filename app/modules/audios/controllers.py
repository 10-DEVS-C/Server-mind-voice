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
from app.modules.folders.services import FolderService
from app.modules.tags.services import TagService

blp = Blueprint("audios", __name__, description="Operations on audios")


def _validate_audio_relations(data):
    current_user = get_current_user_id()
    folder_id = data.get("folderId") if "folderId" in data else None

    if "folderId" in data and folder_id:
        folder = FolderService.get_by_id(folder_id)
        if not folder:
            abort(400, message="Folder no existe")
        if str(folder.get("userId")) != str(current_user) and not is_admin():
            abort(403, message="No tienes permisos sobre esa carpeta")

    if "tagIds" not in data:
        return

    tag_ids = data.get("tagIds") or []
    validated_tag_ids = []

    for tag_id in tag_ids:
        tag = TagService.get_by_id(tag_id)
        if not tag:
            abort(400, message=f"Tag inválido: {tag_id}")

        tag_user_id = tag.get("userId")
        if tag_user_id is not None and str(tag_user_id) != str(current_user) and not is_admin():
            abort(403, message=f"No tienes permisos sobre el tag: {tag_id}")

        validated_tag_ids.append(tag_id)

    data["tagIds"] = validated_tag_ids

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
        _validate_audio_relations(new_data)
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
        try:
            duration_value = int(duration)
            if duration_value < 0:
                abort(400, message="Duration must be >= 0")
        except ValueError:
            abort(400, message="Duration must be an integer")

        title = request.form.get("title") or audio_file.filename
        transcription = request.form.get("transcription")
        folder_id = request.form.get("folderId")
        raw_tag_ids = request.form.get("tagIds")
        tag_ids = []
        if raw_tag_ids:
            tag_ids = [tid.strip() for tid in raw_tag_ids.split(",") if tid.strip()]
        extension = os.path.splitext(secure_filename(audio_file.filename))[1] or ".m4a"

        audio_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "audios")
        os.makedirs(audio_dir, exist_ok=True)

        filename = f"{uuid4().hex}{extension}"
        absolute_path = os.path.join(audio_dir, filename)
        audio_file.save(absolute_path)

        relative_path = f"audios/{filename}"
        audio_data = {
            "userId": get_current_user_id(),
            "title": title,
            "filePath": relative_path,
            "duration": duration_value,
            "format": extension.replace(".", "") or "m4a",
            "transcription": transcription,
            "folderId": folder_id,
            "tagIds": tag_ids,
        }

        _validate_audio_relations(audio_data)
        audio_id = AudioService.create(audio_data)
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
        _validate_audio_relations(update_data)

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
