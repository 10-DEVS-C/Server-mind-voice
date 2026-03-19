from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import FileSchema
from .services import FileService
from app.core.auth_utils import is_admin, get_current_user_id, check_ownership

blp = Blueprint("files", __name__, description="Operations on files")

@blp.route("/")
class FileList(MethodView):
    @blp.response(200, FileSchema(many=True))
    @jwt_required()
    def get(self):
        """List all files"""
        query = {} if is_admin() else {"userId": ObjectId(get_current_user_id())}
        return FileService.get_all(query)

    @blp.arguments(FileSchema)
    @blp.response(201, FileSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new file"""
        if not is_admin() or 'userId' not in new_data:
            new_data['userId'] = get_current_user_id()
        file_id = FileService.create(new_data)
        return FileService.get_by_id(file_id)

@blp.route("/<string:file_id>")
class FileResource(MethodView):
    @blp.response(200, FileSchema)
    @jwt_required()
    def get(self, file_id):
        """Get file by ID"""
        file = FileService.get_by_id(file_id)
        if not file:
            abort(404, message="File not found")
        check_ownership(file)
        return file

    @blp.arguments(FileSchema)
    @blp.response(200, FileSchema)
    @jwt_required()
    def put(self, update_data, file_id):
        """Update existing file"""
        file = FileService.get_by_id(file_id)
        if not file:
            abort(404, message="File not found")
        check_ownership(file)
        
        if not FileService.update(file_id, update_data):
            abort(404, message="File not found")
        return FileService.get_by_id(file_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, file_id):
        """Delete file (soft delete)"""
        file = FileService.get_by_id(file_id)
        if not file:
            abort(404, message="File not found")
        check_ownership(file)
        
        # We can implement soft delete or hard delete based on preference.
        # Requirement says "deleted: Boolean", so let's do soft delete update
        if not FileService.update(file_id, {"deleted": True}):
            abort(404, message="File not found")
        return ""
