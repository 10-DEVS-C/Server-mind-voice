from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "status": "error",
            "message": e.description,
            "code": e.code
        }
        return jsonify(response), e.code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        response = {
            "status": "error",
            "message": "Validation Error",
            "errors": e.messages
        }
        return jsonify(response), 400

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled Exception: {e}")
        response = {
            "status": "error",
            "message": "Internal Server Error",
            "code": 500
        }
        if app.debug:
            response["details"] = str(e)
        return jsonify(response), 500
