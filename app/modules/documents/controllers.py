from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from bson import ObjectId
from .schemas import DocumentSchema
from .services import DocumentService
from app.core.auth_utils import is_admin, get_current_user_id, check_ownership

blp = Blueprint("documents", __name__, description="Operations on documents")

@blp.route("/")
class DocumentList(MethodView):
    @blp.response(200, DocumentSchema(many=True))
    @jwt_required()
    def get(self):
        """List all documents"""
        query = {} if is_admin() else {"userId": ObjectId(get_current_user_id())}
        return DocumentService.get_all(query)

    @blp.arguments(DocumentSchema)
    @blp.response(201, DocumentSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new document"""
        if not is_admin() or 'userId' not in new_data:
            new_data['userId'] = get_current_user_id()
        document_id = DocumentService.create(new_data)
        return DocumentService.get_by_id(document_id)

@blp.route("/<string:document_id>")
class DocumentResource(MethodView):
    @blp.response(200, DocumentSchema)
    @jwt_required()
    def get(self, document_id):
        """Get document by ID"""
        document = DocumentService.get_by_id(document_id)
        if not document:
            abort(404, message="Document not found")
        check_ownership(document)
        return document

    @blp.arguments(DocumentSchema)
    @blp.response(200, DocumentSchema)
    @jwt_required()
    def put(self, update_data, document_id):
        """Update existing document"""
        document = DocumentService.get_by_id(document_id)
        if not document:
            abort(404, message="Document not found")
        check_ownership(document)

        if not DocumentService.update(document_id, update_data):
            abort(404, message="Document not found")
        return DocumentService.get_by_id(document_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, document_id):
        """Delete document"""
        document = DocumentService.get_by_id(document_id)
        if not document:
            abort(404, message="Document not found")
        check_ownership(document)

        if not DocumentService.delete(document_id):
            abort(404, message="Document not found")
        return ""
