from marshmallow import Schema, fields

class WsConnectionSchema(Schema):
    url = fields.String(metadata={"description": "URL base del servidor ej: ws://localhost:5000"})
    client = fields.String(metadata={"description": "Requiere Socket.IO (ej. socket.io-client)"})

class WsJoinSessionEventSchema(Schema):
    session_id = fields.String(required=True, metadata={"description": "El ID único del MindMap o documento para agrupar usuarios en una misma sala."})
    username = fields.String(required=False, metadata={"description": "El nombre del usuario para anunciarlo a los demás en la sala."})

class WsEditEventSchema(Schema):
    session_id = fields.String(required=True, metadata={"description": "Id del documento/sala activa."})
    action = fields.String(required=True, metadata={"description": "Acción realizada: ej. ADD_NODE, DELETE_NODE, MOVE_NODE."})
    node_data = fields.Dict(required=False, metadata={"description": "Diccionario JSON arbitrario con los datos modificados del nodo o arista."})
