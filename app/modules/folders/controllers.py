from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import FolderSchema
from .services import FolderService

blp = Blueprint("folders", __name__, description="Operations on folders")

@blp.route("/")
class FolderList(MethodView):
    @blp.response(200, FolderSchema(many=True))
    @jwt_required()
    def get(self):
        """List all folders"""
        return FolderService.get_all()

    @blp.arguments(FolderSchema)
    @blp.response(201, FolderSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new folder"""
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
        return folder

    @blp.arguments(FolderSchema)
    @blp.response(200, FolderSchema)
    @jwt_required()
    def put(self, update_data, folder_id):
        """Update existing folder"""
        if not FolderService.update(folder_id, update_data):
            abort(404, message="Folder not found")
        return FolderService.get_by_id(folder_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, folder_id):
        """Delete folder"""
        if not FolderService.delete(folder_id):
            abort(404, message="Folder not found")
        return ""
