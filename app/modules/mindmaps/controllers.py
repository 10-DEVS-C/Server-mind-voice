from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import MindmapSchema
from .services import MindmapService

blp = Blueprint("mindmaps", __name__, description="Operations on mindmaps")

@blp.route("/")
class MindmapList(MethodView):
    @blp.response(200, MindmapSchema(many=True))
    @jwt_required()
    def get(self):
        """List all mindmaps"""
        return MindmapService.get_all()

    @blp.arguments(MindmapSchema)
    @blp.response(201, MindmapSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new mindmap"""
        mindmap_id = MindmapService.create(new_data)
        return MindmapService.get_by_id(mindmap_id)

@blp.route("/<int:mindmap_id>")
class MindmapResource(MethodView):
    @blp.response(200, MindmapSchema)
    @jwt_required()
    def get(self, mindmap_id):
        """Get mindmap by ID"""
        mindmap = MindmapService.get_by_id(mindmap_id)
        if not mindmap:
            abort(404, message="Mindmap not found")
        return mindmap

    @blp.arguments(MindmapSchema)
    @blp.response(200, MindmapSchema)
    @jwt_required()
    def put(self, update_data, mindmap_id):
        """Update existing mindmap"""
        if not MindmapService.update(mindmap_id, update_data):
            abort(404, message="Mindmap not found")
        return MindmapService.get_by_id(mindmap_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, mindmap_id):
        """Delete mindmap"""
        if not MindmapService.delete(mindmap_id):
            abort(404, message="Mindmap not found")
        return ""
