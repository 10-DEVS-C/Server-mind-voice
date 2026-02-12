from datetime import datetime

class Document:
    def __init__(self, userId, folderId, title, content=None, docType="nota"):
        self.userId = userId
        self.folderId = folderId
        self.title = title
        self.type = docType
        self.content = content or {}
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.userId,
            "folderId": self.folderId,
            "title": self.title,
            "type": self.type,
            "content": self.content,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
