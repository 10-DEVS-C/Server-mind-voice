from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
import json
import base64

from bson import ObjectId
from app.core.auth_utils import get_current_user_id
from app.modules.ai_analyses.services import AiAnalysisService
from app.modules.transcriptions.services import TranscriptionService

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
    @jwt_required()
    def post(self, data):
        """Analyze text with MindVoice AI"""
        print("Llamando a Gemini")
        texto = data.get("text")
        transcription_id = data.get("transcriptionId")
        api_key = data.get("api_key") or GEMINI_API_KEY
        
        # Lógica de base de datos para extraer transcripción
        if transcription_id:
            db_transcription = TranscriptionService.get_by_id(transcription_id)
            if not db_transcription:
                abort(404, message="La transcripcion especificada no existe en la base de datos.")
            if not texto:
                texto = db_transcription.get("text", "")
                
        if not texto:
            abort(400, message="Debes proporcionar 'text' o apuntar a un 'transcriptionId' que contenga texto.")

        try:
            print("API Key: ", api_key)
            print("Texto: ", texto)
            respuesta_raw = MindVoiceService.llamar_gemini_texto(api_key, PROMPT_MAESTRO, texto)
            print("Respuesta de Gemini: ", respuesta_raw)
            resultado_json = json.loads(respuesta_raw)
            
            # GUARDAR EL ANALISIS RESULTANTE
            ai_data = {
                "userId": ObjectId(get_current_user_id()),
                "transcriptionId": ObjectId(transcription_id) if transcription_id else None,
                "result": resultado_json
            }
            AiAnalysisService.create(ai_data)
            
            return resultado_json
        except json.JSONDecodeError:
            abort(500, message="La respuesta de Gemini no fue un JSON válido.")
        except Exception as e:
            abort(500, message=str(e))

@blp.route("/analyze/audio")
class AnalyzeAudioResource(MethodView):
    @blp.response(200)
    @jwt_required()
    def post(self):
        """Transcribe and analyze Voice Audio"""
        if "audio" not in request.files:
            abort(400, message="No se proporcionó un archivo de audio ('audio')")
        audio_file = request.files["audio"]
        api_key = request.form.get("api_key", GEMINI_API_KEY)
        mime_type = audio_file.mimetype or "audio/webm"
        
        try:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            respuesta_raw = MindVoiceService.llamar_gemini_audio(api_key, PROMPT_MAESTRO, audio_base64, mime_type)
            resultado_json = json.loads(respuesta_raw)
            
            # GUARDAR EL ANALISIS MULTIMODAL
            transcription_id = request.form.get("transcriptionId")
            ai_data = {
                "userId": ObjectId(get_current_user_id()),
                "transcriptionId": ObjectId(transcription_id) if transcription_id else None,
                "result": resultado_json
            }
            AiAnalysisService.create(ai_data)
            
            return resultado_json
        except json.JSONDecodeError:
            abort(500, message="La respuesta de Gemini no fue un JSON válido.")
        except Exception as e:
            abort(500, message=str(e))
