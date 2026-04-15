from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from app.core.auth_utils import is_admin, get_current_user_id
from .schemas import AiAnalysisSchema
from .services import AiAnalysisService

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

    @blp.response(204)
    @jwt_required()
    def delete(self, analysis_id):
        """Delete AI analysis"""
        if not AiAnalysisService.delete(analysis_id):
            abort(404, message="AI Analysis not found")
        return ""
