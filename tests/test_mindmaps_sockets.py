import pytest

def test_socket_connection(socket_client):
    """Prueba que un cliente pueda conectarse limpia y existosamente"""
    assert socket_client.is_connected() is True

def test_socket_join_session(socket_client):
    """Prueba unirse a una sesión emite el evento correspondiente a la sala"""
    # Escuchamos los mensajes emitidos por el servidor
    socket_client.get_received() # Limpia la cola de recibidos previos
    
    socket_client.emit('join_session', {'session_id': 'test_room', 'username': 'DevUser'})
    
    received = socket_client.get_received()
    # Buscar si recibimos el evento de 'user_joined' (Notamos que el emisor también se recibe p/pruebas)
    events = [item for item in received if item['name'] == 'user_joined']
    assert len(events) > 0
    assert events[0]['args'][0]['username'] == 'DevUser'
    assert events[0]['args'][0]['session_id'] == 'test_room'

def test_socket_edit_mindmap_broadcast(app, socket_client):
    """Prueba que la edición retransmita datos"""
    # Creamos un segundo cliente simulado para validar el broadcast
    client2 = app.extensions['socketio'].test_client(app)
    
    # Ambos se unen a la misma sala
    socket_client.emit('join_session', {'session_id': 'room_abc'})
    client2.emit('join_session', {'session_id': 'room_abc'})
    
    # Limpiamos memorias
    socket_client.get_received()
    client2.get_received()
    
    # El socket 1 emite una edición
    socket_client.emit('edit_mindmap', {
        'session_id': 'room_abc', 
        'action': 'ADD_NODE', 
        'node_data': {'id': '1'}
    })
    
    # El cliente 2 debió recibir el 'mindmap_updated'
    received_by_2 = client2.get_received()
    updates = [ev for ev in received_by_2 if ev['name'] == 'mindmap_updated']
    assert len(updates) > 0
    assert updates[0]['args'][0]['action'] == 'ADD_NODE'
    
    # Recordatorio: include_self=False hace que el cliente 1 NO lo reciba
    received_by_1 = socket_client.get_received()
    updates_for_1 = [ev for ev in received_by_1 if ev['name'] == 'mindmap_updated']
    assert len(updates_for_1) == 0

    client2.disconnect()
