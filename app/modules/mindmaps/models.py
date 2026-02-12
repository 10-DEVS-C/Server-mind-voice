from datetime import datetime

class Mindmap:
    def __init__(self, documentId, nodes=None):
        self.documentId = documentId
        self.nodes = nodes or {}
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "documentId": self.documentId,
            "nodes": self.nodes,
            "updatedAt": self.updatedAt
        }
