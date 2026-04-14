import pytest
from io import BytesIO

def test_mindvoice_extract_endpoint(client):
    """Prueba el nuevo endpoint de extracción (Simula subida de archivo .txt)"""
    data = {
        'file': (BytesIO(b'Hola, esto es una prueba de texto.'), 'prueba.txt')
    }
    response = client.post('/mindvoice-api/extract', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'extracted_text' in json_data
    assert json_data['extracted_text'] == 'Hola, esto es una prueba de texto.'

def test_mindvoice_extract_missing_file(client):
    """Prueba que tire error 400 si no mandamos el file"""
    response = client.post('/mindvoice-api/extract', data={}, content_type='multipart/form-data')
    assert response.status_code == 400

def test_mindvoice_analyze_text_schema_validation(client):
    """Prueba que se requiera la propiedad text en el endpoint Gemini"""
    response = client.post('/mindvoice-api/analyze/text', json={})
    assert response.status_code == 422  # Marshmallow detecta que falta texto
