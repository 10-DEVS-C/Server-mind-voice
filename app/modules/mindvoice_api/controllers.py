from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
import json
import base64

from bson import ObjectId
from app.core.auth_utils import get_current_user_id, check_ownership
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
        texto = data.get("text")
        transcription_id = data.get("transcriptionId")
        api_key = data.get("api_key") or GEMINI_API_KEY
        
        # Lógica de base de datos para extraer transcripción
        if transcription_id:
            db_transcription = TranscriptionService.get_by_id(transcription_id)
            if not db_transcription:
                abort(404, message="La transcripcion especificada no existe en la base de datos.")
            check_ownership(db_transcription)
            if not texto:
                texto = db_transcription.get("text", "")
                
        if not texto:
            abort(400, message="Debes proporcionar 'text' o apuntar a un 'transcriptionId' que contenga texto.")

        try:
            respuesta_raw = MindVoiceService.llamar_gemini_texto(api_key, PROMPT_MAESTRO, texto)
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
        print("Analizando audio...")
        if "audio" not in request.files:
            abort(400, message="No se proporcionó un archivo de audio ('audio')")
        
        audio_file = request.files["audio"]
        api_key = request.form.get("api_key", GEMINI_API_KEY)
        
        # --- CORRECCIÓN DE MIME TYPE ---
        # Derivar el MIME type correcto según la extensión del archivo.
        import os as _os
        ext = _os.path.splitext(audio_file.filename or '')[1].lower()
        _ext_mime = {
            '.m4a': 'audio/mp4',
            '.mp4': 'audio/mp4',
            '.mp3': 'audio/mp3',
            '.mpeg': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.aac': 'audio/aac',
            '.ogg': 'audio/ogg',
            '.flac': 'audio/flac',
            '.webm': 'audio/webm',
            '.opus': 'audio/opus',
        }
        incoming_mime = audio_file.mimetype or ""
        # Priorizar extensión sobre MIME declarado (los clientes móviles son poco fiables)
        mime_type = _ext_mime.get(ext) or (incoming_mime if incoming_mime and 'video' not in incoming_mime else None) or 'audio/mp4'
        
        print(f"Procesando audio con MIME: {mime_type}")
        
        try:
            audio_file.seek(0) # Asegurar que estamos al inicio del archivo
            audio_bytes = audio_file.read()
            
            if len(audio_bytes) == 0:
                abort(400, message="El archivo de audio está vacío.")

            print(f"Audio leído: {len(audio_bytes)} bytes")
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            
            respuesta_raw = MindVoiceService.llamar_gemini_audio(api_key, PROMPT_MAESTRO, audio_base64, mime_type)
            
            # Si Gemini devuelve un error o vacío
            if not respuesta_raw or respuesta_raw == "{}":
                abort(500, message="Gemini no pudo procesar el audio.")

            resultado_json = json.loads(respuesta_raw)
            
            # --- GUARDAR EN BD ---
            transcription_id = request.form.get("transcriptionId")
            if transcription_id:
                db_transcription = TranscriptionService.get_by_id(transcription_id)
                if db_transcription:
                    check_ownership(db_transcription)

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
            print(f"Error crítico: {str(e)}")
            abort(500, message=str(e))