from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import TagSchema
from .services import TagService

blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    @jwt_required()
    def get(self):
        """List all tags"""
        return TagService.get_all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new tag"""
        tag_id = TagService.create(new_data)
        return TagService.get_by_id(tag_id)

@blp.route("/<int:tag_id>")
class TagResource(MethodView):
    @blp.response(200, TagSchema)
    @jwt_required()
    def get(self, tag_id):
        """Get tag by ID"""
        tag = TagService.get_by_id(tag_id)
        if not tag:
            abort(404, message="Tag not found")
        return tag
    
    @blp.response(204)
    @jwt_required()
    def delete(self, tag_id):
        """Delete tag"""
        if not TagService.delete(tag_id):
            abort(404, message="Tag not found")
        return ""
