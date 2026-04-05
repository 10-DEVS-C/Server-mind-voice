import pytest

def test_auth_swagger_docs_accessible(client):
    """Prueba que el servidor expone su documentación (indica que la app levanta bien)"""
    response = client.get('/swagger-ui')
    # Podría redireccionar o devolver HTML
    assert response.status_code in [200, 301, 302, 308]

def test_auth_login_validation(client):
    """
    Prueba que el endpoint rest de users/auth responde correctamente
    (Asume que responde 4xx o 422 si la data está en blanco)
    """
    response = client.post('/auth/login', json={})
    assert response.status_code >= 400  # Fallo validado correctamente
