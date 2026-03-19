from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import SessionSchema
from .services import SessionService
from app.core.auth_utils import is_admin, get_current_user_id, check_ownership

blp = Blueprint("sessions", __name__, description="Operations on sessions")

@blp.route("/")
class SessionList(MethodView):
    @blp.response(200, SessionSchema(many=True))
    @jwt_required()
    def get(self):
        """List all sessions"""
        query = {} if is_admin() else {"userId": ObjectId(get_current_user_id())}
        return SessionService.get_all(query)

    @blp.arguments(SessionSchema)
    @blp.response(201, SessionSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new session"""
        if not is_admin() or 'userId' not in new_data:
            new_data['userId'] = get_current_user_id()
        session_id = SessionService.create(new_data)
        return SessionService.get_by_id(session_id)

@blp.route("/<string:session_id>")
class SessionResource(MethodView):
    @blp.response(200, SessionSchema)
    @jwt_required()
    def get(self, session_id):
        """Get session by ID"""
        session = SessionService.get_by_id(session_id)
        if not session:
            abort(404, message="Session not found")
        check_ownership(session)
        return session
    
    @blp.response(204)
    @jwt_required()
    def delete(self, session_id):
        """Delete session"""
        session = SessionService.get_by_id(session_id)
        if not session:
            abort(404, message="Session not found")
        check_ownership(session)
        
        if not SessionService.delete(session_id):
            abort(404, message="Session not found")
        return ""
