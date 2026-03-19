from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import ActivityLogSchema
from .services import ActivityLogService
from app.core.auth_utils import is_admin, get_current_user_id, check_ownership

blp = Blueprint("activity_logs", __name__, description="Operations on activity logs")

@blp.route("/")
class ActivityLogList(MethodView):
    @blp.response(200, ActivityLogSchema(many=True))
    @jwt_required()
    def get(self):
        """List all activity logs"""
        query = {} if is_admin() else {"userId": ObjectId(get_current_user_id())}
        return ActivityLogService.get_all(query)

    @blp.arguments(ActivityLogSchema)
    @blp.response(201, ActivityLogSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new activity log"""
        if not is_admin() or 'userId' not in new_data:
            new_data['userId'] = get_current_user_id()
        log_id = ActivityLogService.create(new_data)
        return ActivityLogService.get_by_id(log_id)

@blp.route("/<string:log_id>")
class ActivityLogResource(MethodView):
    @blp.response(200, ActivityLogSchema)
    @jwt_required()
    def get(self, log_id):
        """Get activity log by ID"""
        log = ActivityLogService.get_by_id(log_id)
        if not log:
            abort(404, message="Activity Log not found")
        check_ownership(log)
        return log
