from datetime import datetime

class Mindmap:
    def __init__(self, document_id, nodes=None):
        self.document_id = document_id
        self.nodes = nodes or {}
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "documentId": self.document_id,
            "nodes": self.nodes,
            "updated_at": self.updated_at
        }
