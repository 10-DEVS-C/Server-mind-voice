from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from .schemas import DocumentSchema
from .services import DocumentService

blp = Blueprint("documents", __name__, description="Operations on documents")

@blp.route("/")
class DocumentList(MethodView):
    @blp.response(200, DocumentSchema(many=True))
    @jwt_required()
    def get(self):
        """List all documents"""
        return DocumentService.get_all()

    @blp.arguments(DocumentSchema)
    @blp.response(201, DocumentSchema)
    @jwt_required()
    def post(self, new_data):
        """Create a new document"""
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
        return document

    @blp.arguments(DocumentSchema)
    @blp.response(200, DocumentSchema)
    @jwt_required()
    def put(self, update_data, document_id):
        """Update existing document"""
        if not DocumentService.update(document_id, update_data):
            abort(404, message="Document not found")
        return DocumentService.get_by_id(document_id)

    @blp.response(204)
    @jwt_required()
    def delete(self, document_id):
        """Delete document"""
        if not DocumentService.delete(document_id):
            abort(404, message="Document not found")
        return ""
