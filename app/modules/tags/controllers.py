from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import TagSchema, TagQueryArgsSchema
from .services import TagService
from app.core.auth_utils import is_admin, get_current_user_id

blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route("/")
class TagList(MethodView):
    @blp.arguments(TagQueryArgsSchema, location="query")
    @blp.response(200, TagSchema(many=True))
    @jwt_required()
    def get(self, query_args):
        """List tags: Global tags (no userId) + User's tags"""
        if is_admin():
            return TagService.get_all()
            
        user_id = ObjectId(get_current_user_id())
        query = {"$or": [{"userId": None}, {"userId": {"$exists": False}}, {"userId": user_id}]}
        return TagService.get_all(query)

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new tag"""
        if is_admin():
            new_data['userId'] = None
        else:
            new_data['userId'] = ObjectId(get_current_user_id())
            
        tag_id = TagService.create(new_data)
        return TagService.get_by_id(tag_id)

@blp.route("/<string:tag_id>")
class TagResource(MethodView):
    @blp.response(200, TagSchema)
    @jwt_required()
    def get(self, tag_id):
        """Get tag by ID"""
        tag = TagService.get_by_id(tag_id)
        if not tag:
            abort(404, message="Tag not found")
            
        current_user = get_current_user_id()
        if tag.get('userId') is not None and str(tag.get('userId')) != current_user and not is_admin():
            abort(403, message="Access denied")
            
        return tag
    
    @blp.response(204)
    @jwt_required()
    def delete(self, tag_id):
        """Delete tag"""
        tag = TagService.get_by_id(tag_id)
        if not tag:
            abort(404, message="Tag not found")
            
        current_user = get_current_user_id()
        
        # Admin can delete anything. Users can only delete their own.
        if tag.get('userId') is None and not is_admin():
            abort(403, message="Only admins can delete global tags")
            
        if tag.get('userId') is not None and str(tag.get('userId')) != current_user and not is_admin():
            abort(403, message="Access denied")
            
        if not TagService.delete(tag_id):
            abort(404, message="Tag not found")
        return ""
