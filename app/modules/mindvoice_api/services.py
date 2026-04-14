import os
import requests

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

GEMINI_API_KEY = os.getenv("VITE_GEMINI_API_KEY", "")
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

class MindVoiceService:
    @staticmethod
    def extraer_texto_de_archivo(file_obj, filename):
        ext = filename.lower().split('.')[-1]
        if ext in ["txt", "md", "csv", "json"]:
            return file_obj.read().decode("utf-8", errors="ignore")
        elif ext == "pdf":
            if not HAS_PYPDF2:
                raise Exception("Librería PyPDF2 no instalada.")
            reader = PyPDF2.PdfReader(file_obj)
            pages = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    pages.append(f"Página {i+1}\n{text}")
            return "\n\n".join(pages)
        elif ext == "docx":
            if not HAS_DOCX:
                raise Exception("Librería python-docx no instalada.")
            doc = docx.Document(file_obj)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            raise Exception("Formato no soportado.")

    @staticmethod
    def llamar_gemini_texto(api_key, prompt, extracted_text, model=GEMINI_MODEL):
        if not api_key:
            raise ValueError("Se requiere una API Key de Gemini válida.")


        
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        body = {
            "contents": [{"role": "user", "parts": [{"text": f"{prompt}\n\nCONTENIDO A ANALIZAR:\n{extracted_text}"}] }],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}
        }
        res = requests.post(endpoint, headers={"Content-Type": "application/json"}, json=body)
        if not res.ok:
            raise Exception(f"Gemini devolvió {res.status_code}: {res.text}")
        try:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "{}"

    @staticmethod
    def llamar_gemini_audio(api_key, prompt, audio_base64, mime_type, model=GEMINI_MODEL):
        if not api_key:
            raise ValueError("Se requiere una API Key de Gemini válida.")
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        body = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{prompt}\n\nEste input es audio. Primero transcribe y luego analiza."},
                        {"inlineData": {"mimeType": mime_type, "data": audio_base64}}
                    ]
                }
            ],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}
        }
        res = requests.post(endpoint, headers={"Content-Type": "application/json"}, json=body)
        if not res.ok:
            raise Exception(f"Gemini devolvió {res.status_code}: {res.text}")
        try:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "{}"
