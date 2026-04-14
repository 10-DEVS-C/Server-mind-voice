from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from .schemas import WsConnectionSchema, WsJoinSessionEventSchema, WsEditEventSchema

blp = Blueprint("mindmaps_sockets", __name__, description="WebSockets Mindmaps Collaboration (Solo Documentación/Guía)")

@blp.route("/info")
class WsConnectDocs(MethodView):
    @blp.response(200, WsConnectionSchema)
    def get(self):
        """1. Información de conexión WebSocket
        
        NOTA IMPORTANTÍSIMA: Esta API de WebSockets no funciona a través de peticiones HTTP tradicionales.
        Debes inicializar una conexión asíncrona real desde el frontend utilizando `socket.io-client` 
        apuntando a la URL principal del servidor. Estos endpoints están aquí únicamente para documentar los contratos.
        """
        return {"url": "wss://tu-servidor.com", "client": "socket.io-client estándar"}

@blp.route("/events/join-session")
class WsJoinSessionDocs(MethodView):
    @blp.arguments(WsJoinSessionEventSchema)
    def post(self, data):
        """2. Evento WebSocket: join_session / leave_session
        
        CÓMO USAR EN FRONTEND:
        - socket.emit('join_session', { session_id: "...", username: "..." });
        
        QUÉ DEVUELVE EL SERVIDOR (escuchar):
        - socket.on('user_joined', (res) => { ... })
        - socket.on('user_left', (res) => { ... })
        
        *Nota: Este Endpoint HTTP es solo ilustrativo.*
        """
        return jsonify({"message": "Documentación. En produccion, emite vía WebSockets."}), 200

@blp.route("/events/edit-mindmap")
class WsEditMindmapDocs(MethodView):
    @blp.arguments(WsEditEventSchema)
    def post(self, data):
        """3. Evento WebSocket: edit_mindmap
        
        Transmite una modificación en el lienzo a toda la sala de trabajo en menos de 100ms.
        
        CÓMO USAR EN FRONTEND:
        - socket.emit('edit_mindmap', { session_id: "...", action: "ADD_NODE", node_data: {...} });
        
        QUÉ DEVUELVE EL SERVIDOR (escuchar):
        - socket.on('mindmap_updated', (res) => { ... }) (Todos en la sala reciben el cambio de forma automática).
        
        *Nota: Este Endpoint HTTP es solo ilustrativo.*
        """
        return jsonify({"message": "Documentación. En produccion, emite vía WebSockets."}), 200
