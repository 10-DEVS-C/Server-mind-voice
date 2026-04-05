import pytest
import json

def test_get_folders_unauthorized(client):
    """Prueba que los módulos base estén bajo protección de sesion/JWT por defecto"""
    response = client.get('/folders/')
    assert response.status_code == 401  # Missing Authorization Header

def test_create_folder_validation(client):
    """Prueba que el framework smorest arroje validaciones correctas (422) o de Auth (401)"""
    response = client.post('/folders/', json={"invalid": "data"})
    assert response.status_code in [401, 422]
