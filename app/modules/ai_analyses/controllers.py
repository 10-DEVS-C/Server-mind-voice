from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from app.core.auth_utils import is_admin, get_current_user_id, check_ownership
from app.extensions import mongo
from .schemas import AiAnalysisSchema
from .services import AiAnalysisService

PRO_PLANS = {"professional", "business"}

blp = Blueprint("ai_analyses", __name__, description="Operations on AI analyses")

@blp.route("/")
class AiAnalysisList(MethodView):
    @blp.response(200, AiAnalysisSchema(many=True))
    @jwt_required()
    def get(self):
        """List all AI analyses"""
        query = {} if is_admin() else {"userId": ObjectId(get_current_user_id())}
        t_id = request.args.get("transcriptionId")
        if t_id:
            query["transcriptionId"] = ObjectId(t_id)
        return AiAnalysisService.get_all(query)

    @blp.arguments(AiAnalysisSchema)
    @blp.response(201, AiAnalysisSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new AI analysis"""
        analysis_id = AiAnalysisService.create(new_data)
        return AiAnalysisService.get_by_id(analysis_id)

@blp.route("/<string:analysis_id>")
class AiAnalysisResource(MethodView):
    @blp.response(200, AiAnalysisSchema)
    @jwt_required()
    def get(self, analysis_id):
        """Get AI analysis by ID"""
        analysis = AiAnalysisService.get_by_id(analysis_id)
        if not analysis:
            abort(404, message="AI Analysis not found")
        return analysis

    @blp.arguments(AiAnalysisSchema(partial=True))
    @blp.response(200, AiAnalysisSchema)
    @jwt_required()
    def put(self, update_data, analysis_id):
        """Update AI analysis result (requires professional or business plan)"""
        analysis = AiAnalysisService.get_by_id(analysis_id)
        if not analysis:
            abort(404, message="AI Analysis not found")
        check_ownership(analysis)

        if not is_admin():
            user_id = get_current_user_id()
            user = mongo.db["users"].find_one({"_id": ObjectId(user_id)})
            user_plan = (user or {}).get("plan", "basic")
            if user_plan not in PRO_PLANS:
                abort(403, message="Esta función requiere un plan profesional o business")

        update_data.pop("userId", None)
        update_data.pop("transcriptionId", None)
        if not AiAnalysisService.update(analysis_id, update_data):
            abort(404, message="AI Analysis not found")
        return AiAnalysisService.get_by_id(analysis_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, analysis_id):
        """Delete AI analysis"""
        if not AiAnalysisService.delete(analysis_id):
            abort(404, message="AI Analysis not found")
        return ""
