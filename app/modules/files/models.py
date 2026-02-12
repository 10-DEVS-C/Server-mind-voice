from datetime import datetime

class File:
    def __init__(self, user_id, folder_id, title, tag_ids=None, file_type="txt"):
        self.user_id = user_id
        self.folder_id = folder_id
        self.title = title
        self.type = file_type
        self.tag_ids = tag_ids or []
        self.deleted = False
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.user_id,
            "folderId": self.folder_id,
            "title": self.title,
            "type": self.type,
            "tagIds": self.tag_ids,
            "deleted": self.deleted,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
