from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
import json
import base64

from .schemas import AnalyzeTextSchema, ExtractTextResponseSchema
from .services import MindVoiceService, GEMINI_API_KEY, PROMPT_MAESTRO

blp = Blueprint("mindvoice_api", __name__, description="Integrated Prototype APIs")

@blp.route("/extract")
class ExtractFileResource(MethodView):
    @blp.response(200, ExtractTextResponseSchema)
    # @jwt_required() # Descomentar cuando desees restringir el acceso con JWT
    def post(self):
        """Extract text from a document
        
        Reads text from TXT, MD, CSV, JSON, PDF, or DOCX files uploaded as 'file' form-data.
        """
        if "file" not in request.files:
            abort(400, message="No se proporcionó un archivo ('file')")
        file = request.files["file"]
        if not file.filename:
            abort(400, message="Nombre de archivo vacío")
        try:
            texto = MindVoiceService.extraer_texto_de_archivo(file, file.filename)
            return {"extracted_text": texto}
        except Exception as e:
            abort(400, message=str(e))

@blp.route("/analyze/text")
class AnalyzeTextResource(MethodView):
    @blp.arguments(AnalyzeTextSchema)
    @blp.response(200)
    # @jwt_required()
    def post(self, data):
        """Analyze text with MindVoice AI
        
        Uses Gemini to generate the structured JSON MindVoice response given raw text.
        """
        texto = data["text"]
        api_key = data.get("api_key") or GEMINI_API_KEY
        try:
            respuesta_raw = MindVoiceService.llamar_gemini_texto(api_key, PROMPT_MAESTRO, texto)
            return json.loads(respuesta_raw)
        except json.JSONDecodeError:
            abort(500, message="La respuesta de Gemini no fue un JSON válido.")
        except Exception as e:
            abort(500, message=str(e))

@blp.route("/analyze/audio")
class AnalyzeAudioResource(MethodView):
    @blp.response(200)
    # @jwt_required()
    def post(self):
        """Transcribe and analyze Voice Audio
        
        Upload audio file as 'audio' form-data to extract the structured MindVoice info via Gemini.
        """
        if "audio" not in request.files:
            abort(400, message="No se proporcionó un archivo de audio ('audio')")
        audio_file = request.files["audio"]
        api_key = request.form.get("api_key", GEMINI_API_KEY)
        mime_type = audio_file.mimetype or "audio/webm"
        
        try:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            respuesta_raw = MindVoiceService.llamar_gemini_audio(api_key, PROMPT_MAESTRO, audio_base64, mime_type)
            return json.loads(respuesta_raw)
        except json.JSONDecodeError:
            abort(500, message="La respuesta de Gemini no fue un JSON válido.")
        except Exception as e:
            abort(500, message=str(e))
