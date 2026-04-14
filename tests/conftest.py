import pytest
from app import create_app
from app.extensions import socketio

@pytest.fixture
def app():
    # Configuramos la app en modo TESTING y usamos mongomock en memoria
    # para que las pruebas no afecten a la base de datos real.
    app = create_app()
    app.config.update({
        "TESTING": True,
        "MONGO_URI": "mongomock://localhost:27017/mindvoice_test",
        "JWT_SECRET_KEY": "super_secret_test_key"
    })
    
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Cliente HTTP para testear rutas REST"""
    return app.test_client()

@pytest.fixture
def socket_client(app):
    """Cliente SocketIO para testear WebSockets"""
    client = socketio.test_client(app)
    yield client
    if client.is_connected():
        client.disconnect()
