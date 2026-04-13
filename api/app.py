import os
import json
import base64
import requests
from flask import Flask, request, jsonify

# Para manejar subidas de documentos:
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

app = Flask(__name__)

# Configuraciones de Gemini
# Usa la variable de entorno, si no existe o necesitas forzar una por defecto, agrégala.
GEMINI_API_KEY = os.environ.get("VITE_GEMINI_API_KEY", "") 
GEMINI_MODEL = "gemini-2.5-flash"

PROMPT_MAESTRO = """Eres el motor de análisis de MindVoice AI.

Objetivo:
1. Recibir audio o texto transcrito.
2. Transcribir si el input es audio.
3. Permitir corrección manual previa al análisis.
4. Generar una salida estructurada para MindVoice.
5. Producir resumen ejecutivo en 3 párrafos, tareas, insights y nodos para mapa mental.

Devuelve JSON válido con esta forma:
{
  "title": "",
  "transcription": "",
  "transcription_with_timestamps": [
    { "start": "00:00", "end": "00:05", "text": "" }
  ],
  "executive_summary": ["", "", ""],
  "edited_text": "",
  "key_insights": [""],
  "task_list": [{ "task": "", "priority": "baja|media|alta" }],
  "mind_map_nodes": [{ "id": "", "label": "", "parentId": null }],
  "tags": [""],
  "semantic_keywords": [""],
  "report_ready_text": ""
}

Reglas:
- No inventes hechos.
- Si falta información, indícalo.
- El resumen ejecutivo debe tener exactamente 3 párrafos.
- Las tareas deben devolverse como array de objetos {task, priority}.
- Los nodos del mapa mental deben estar listos para renderizar con Mermaid.js o librerías similares.
- Si puedes, devuelve transcription_with_timestamps por frase en JSON."""

def extraer_texto_de_archivo(file_obj, filename):
    """Extrae texto de archivos TXT, MD, CSV, JSON, PDF, o DOCX"""
    ext = filename.lower().split('.')[-1]
    
    if ext in ["txt", "md", "csv", "json"]:
        return file_obj.read().decode("utf-8", errors="ignore")
        
    elif ext == "pdf":
        if not HAS_PYPDF2:
            raise Exception("Librería PyPDF2 no instalada. (Ejecuta: pip install PyPDF2)")
        reader = PyPDF2.PdfReader(file_obj)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(f"Página {i+1}\n{text}")
        return "\n\n".join(pages)
        
    elif ext == "docx":
        if not HAS_DOCX:
            raise Exception("Librería python-docx no instalada. (Ejecuta: pip install python-docx)")
        doc = docx.Document(file_obj)
        return "\n".join([para.text for para in doc.paragraphs])
        
    else:
        raise Exception("Formato no soportado. Usa TXT, MD, CSV, JSON, PDF o DOCX.")


def llamar_gemini_texto(api_key, prompt, extracted_text, model=GEMINI_MODEL):
    """Llama a la IA de Gemini para procesar texto"""
    if not api_key:
        raise ValueError("Se requiere una API Key de Gemini válida.")
        
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"{prompt}\n\nCONTENIDO A ANALIZAR:\n{extracted_text}"
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }
    
    res = requests.post(
        endpoint,
        headers={"Content-Type": "application/json"},
        json=body
    )
    
    if not res.ok:
        raise Exception(f"Gemini devolvió {res.status_code}: {res.text}")
        
    data = res.json()
    try:
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return content
    except (KeyError, IndexError):
        return "{}"


def llamar_gemini_audio(api_key, prompt, audio_base64, mime_type, model=GEMINI_MODEL):
    """Llama a la IA de Gemini para transcribir y procesar audio"""
    if not api_key:
        raise ValueError("Se requiere una API Key de Gemini válida.")
        
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": f"{prompt}\n\nEste input es audio. Primero transcribe y luego analiza."
                    },
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": audio_base64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }
    
    res = requests.post(
        endpoint,
        headers={"Content-Type": "application/json"},
        json=body
    )
    
    if not res.ok:
        raise Exception(f"Gemini devolvió {res.status_code}: {res.text}")
        
    data = res.json()
    try:
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        return content
    except (KeyError, IndexError):
        return "{}"


@app.route("/api/extract", methods=["POST"])
def endpoint_extract():
    """Ruta para extraer texto de archivos previo al análisis IA (Equivalente UI: Subir archivo)"""
    if "file" not in request.files:
        return jsonify({"error": "No se proporcionó un archivo ('file')."}), 400
        
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Nombre de archivo vacío."}), 400
        
    try:
        texto = extraer_texto_de_archivo(file, file.filename)
        return jsonify({"extracted_text": texto})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/analyze/text", methods=["POST"])
def endpoint_analyze_text():
    """Ruta principal para procesar texto usando Gemini IA"""
    print("Llamando a endpoint_analyze_text") 
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Se esperaba JSON con propiedad 'text'."}), 400
        
    texto = data["text"]
    api_key = data.get("api_key", GEMINI_API_KEY)
    
    try:
        # Llamar a Gemini Text
        print("Llamando a Gemini Text")
        respuesta_raw = llamar_gemini_texto(api_key, PROMPT_MAESTRO, texto)
        print("Respuesta de Gemini Text: ", respuesta_raw)
        # Parseamos el JSON seguro
        resultado = json.loads(respuesta_raw)
        return jsonify(resultado)
        
    except json.JSONDecodeError:
        return jsonify({"error": "La respuesta de Gemini no fue un JSON válido.", "raw_response": respuesta_raw}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/analyze/audio", methods=["POST"])
def endpoint_analyze_audio():
    """Ruta principal para transcribir y procesar audio usando Gemini IA"""
    if "audio" not in request.files:
        return jsonify({"error": "No se proporcionó un archivo de audio ('audio') en los datos form-data."}), 400
        
    audio_file = request.files["audio"]
    # Podrían mandar el api_key opcional
    api_key = request.form.get("api_key", GEMINI_API_KEY)
    
    mime_type = audio_file.mimetype or "audio/webm"
    
    try:
        audio_bytes = audio_file.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        
        # Llamar a Gemini Audio
        respuesta_raw = llamar_gemini_audio(api_key, PROMPT_MAESTRO, audio_base64, mime_type)
        
        resultado = json.loads(respuesta_raw)
        return jsonify(resultado)
        
    except json.JSONDecodeError:
        return jsonify({"error": "La respuesta de Gemini no fue un JSON válido.", "raw_response": respuesta_raw}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Iniciando MindVoice API Server en el puerto 5001...")
    app.run(debug=True, port=5001)
