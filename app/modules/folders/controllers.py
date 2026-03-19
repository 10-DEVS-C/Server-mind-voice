from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import FolderSchema
from .services import FolderService
from app.core.auth_utils import is_admin, get_current_user_id, check_ownership

blp = Blueprint("folders", __name__, description="Operations on folders")

@blp.route("/")
class FolderList(MethodView):
    @blp.response(200, FolderSchema(many=True))
    @jwt_required()
    def get(self):
        """List all folders"""
        query = {} if is_admin() else {"userId": ObjectId(get_current_user_id())}
        return FolderService.get_all(query)

    @blp.arguments(FolderSchema)
    @blp.response(201, FolderSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new folder"""
        if not is_admin() or 'userId' not in new_data:
            new_data['userId'] = get_current_user_id()
        folder_id = FolderService.create(new_data)
        return FolderService.get_by_id(folder_id)

@blp.route("/<string:folder_id>")
class FolderResource(MethodView):
    @blp.response(200, FolderSchema)
    @jwt_required()
    def get(self, folder_id):
        """Get folder by ID"""
        folder = FolderService.get_by_id(folder_id)
        if not folder:
            abort(404, message="Folder not found")
        check_ownership(folder)
        return folder

    @blp.arguments(FolderSchema)
    @blp.response(200, FolderSchema)
    @jwt_required()
    def put(self, update_data, folder_id):
        """Update existing folder"""
        folder = FolderService.get_by_id(folder_id)
        if not folder:
            abort(404, message="Folder not found")
        check_ownership(folder)
        
        if not FolderService.update(folder_id, update_data):
            abort(404, message="Folder not found")
        return FolderService.get_by_id(folder_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, folder_id):
        """Delete folder"""
        folder = FolderService.get_by_id(folder_id)
        if not folder:
            abort(404, message="Folder not found")
        check_ownership(folder)
        
        if not FolderService.delete(folder_id):
            abort(404, message="Folder not found")
        return ""
