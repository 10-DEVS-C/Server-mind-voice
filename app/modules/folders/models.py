from datetime import datetime

class Folder:
    def __init__(self, userId, name, parentFolderId=None):
        self.userId = userId
        self.name = name
        self.parentFolderId = parentFolderId
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.userId,
            "name": self.name,
            "parentFolderId": self.parentFolderId,
            "createdAt": self.createdAt
        }
