from datetime import datetime

class Document:
    def __init__(self, user_id, folder_id, title, content=None, doc_type="nota"):
        self.user_id = user_id
        self.folder_id = folder_id
        self.title = title
        self.type = doc_type
        self.content = content or {}
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.user_id,
            "folderId": self.folder_id,
            "title": self.title,
            "type": self.type,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
