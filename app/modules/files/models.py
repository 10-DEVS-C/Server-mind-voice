from datetime import datetime

class File:
    def __init__(self, userId, folderId, title, tagIds=None, fileType="txt"):
        self.userId = userId
        self.folderId = folderId
        self.title = title
        self.type = fileType
        self.tagIds = tagIds or []
        self.deleted = False
        self.createdAt = datetime.utcnow()
        self.updatedAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.userId,
            "folderId": self.folderId,
            "title": self.title,
            "type": self.type,
            "tagIds": self.tagIds,
            "deleted": self.deleted,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }
