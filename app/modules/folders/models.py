from datetime import datetime

class Folder:
    def __init__(self, user_id, name, parent_folder_id=None):
        self.user_id = user_id
        self.name = name
        self.parent_folder_id = parent_folder_id
        self.createdAt = datetime.utcnow()

    def to_dict(self):
        return {
            "userId": self.user_id,
            "name": self.name,
            "parentFolderId": self.parent_folder_id,
            "createdAt": self.createdAt
        }
