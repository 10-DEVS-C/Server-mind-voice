from flask_socketio import emit, join_room, leave_room
from app.extensions import socketio

@socketio.on('connect')
def handle_connect():
    print("Nuevo cliente conectado a MindMap Sockets")

@socketio.on('disconnect')
def handle_disconnect():
    print("Cliente desconectado de MindMap Sockets")

@socketio.on('join_session')
def on_join(data):
    """
    Permite a un usuario unirse a una sesión de edición de un mindmap.
    El cliente debería emitir: {"session_id": "mindmap_123", "username": "user1"}
    """
    session_id = data.get('session_id')
    username = data.get('username', 'Usuario Anónimo')
    
    if not session_id:
        return
    
    join_room(session_id)
    # Notifica a los demás que alguien entró
    emit('user_joined', {
        'username': username, 
        'session_id': session_id,
        'message': f'{username} se ha unido a la sesión de edición'
    }, to=session_id)

@socketio.on('leave_session')
def on_leave(data):
    """
    Permite salir de la sesión actual de edición.
    """
    session_id = data.get('session_id')
    username = data.get('username', 'Usuario Anónimo')
    
    if not session_id:
        return
        
    leave_room(session_id)
    emit('user_left', {
        'username': username,
        'message': f'{username} ha abandonado la sesión'
    }, to=session_id)

@socketio.on('edit_mindmap')
def on_edit_mindmap(data):
    """
    Recibe los cambios en tiempo real del mindmap y los retransmite a la sala.
    El frontend envía el estado nuevo o la acción (ej. mover nodo).
    """
    session_id = data.get('session_id')
    if not session_id:
        return
    
    # Se reenvía a toda la sala de la sesión, EXCEPTO al mismo que emitió el evento.
    emit('mindmap_updated', data, to=session_id, include_self=False)

@socketio.on('share_mindmap')
def on_share_mindmap(data):
    """
    Notifica a otros usuarios que se les ha compartido un documento/mindmap.
    El cliente emite: {"target_user_id": "user_id_456", "document_id": "mindmap_123"}
    """
    target_user_id = data.get('target_user_id')
    document_id = data.get('document_id')
    
    if target_user_id:
        # En diseño avanzado, cada usuario podría tener su propia room = target_user_id
        emit('invitation_received', {
            'document_id': document_id, 
            'message': 'Te han invitado a colaborar en un mapa mental. ¡Únete a la sesión!'
        }, to=target_user_id)
    else:
        # Compartir globalmente si no hay un target específico
        emit('mindmap_public_shared', {
            'document_id': document_id,
            'message': 'Un nuevo mapa mental está disponible para colaborar.'
        }, broadcast=True)
