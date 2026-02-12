from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import ActivityLogSchema
from .services import ActivityLogService

blp = Blueprint("activity_logs", __name__, description="Operations on activity logs")

@blp.route("/")
class ActivityLogList(MethodView):
    @blp.response(200, ActivityLogSchema(many=True))
    @jwt_required()
    def get(self):
        """List all activity logs"""
        return ActivityLogService.get_all()

    @blp.arguments(ActivityLogSchema)
    @blp.response(201, ActivityLogSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new activity log"""
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
        return log
