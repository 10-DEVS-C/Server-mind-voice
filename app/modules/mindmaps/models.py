from datetime import datetime

class Mindmap:
    def __init__(self, document_id, nodes=None):
        self.document_id = document_id
        self.nodes = nodes or {}
        self.nodes = nodes or {}
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "documentId": self.document_id,
            "nodes": self.nodes,
            "updatedAt": self.updatedAt
        }
