from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import FileSchema
from .services import FileService

blp = Blueprint("files", __name__, description="Operations on files")

@blp.route("/")
class FileList(MethodView):
    @blp.response(200, FileSchema(many=True))
    @jwt_required()
    def get(self):
        """List all files"""
        return FileService.get_all()

    @blp.arguments(FileSchema)
    @blp.response(201, FileSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new file"""
        file_id = FileService.create(new_data)
        return FileService.get_by_id(file_id)

@blp.route("/<int:file_id>")
class FileResource(MethodView):
    @blp.response(200, FileSchema)
    @jwt_required()
    def get(self, file_id):
        """Get file by ID"""
        file = FileService.get_by_id(file_id)
        if not file:
            abort(404, message="File not found")
        return file

    @blp.arguments(FileSchema)
    @blp.response(200, FileSchema)
    @jwt_required()
    def put(self, update_data, file_id):
        """Update existing file"""
        if not FileService.update(file_id, update_data):
            abort(404, message="File not found")
        return FileService.get_by_id(file_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, file_id):
        """Delete file (soft delete)"""
        # We can implement soft delete or hard delete based on preference.
        # Requirement says "deleted: Boolean", so let's do soft delete update
        if not FileService.update(file_id, {"deleted": True}):
            abort(404, message="File not found")
        return ""
