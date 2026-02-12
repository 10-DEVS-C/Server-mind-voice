from bson import ObjectId
from app.extensions import mongo
from typing import List, Optional, Dict, Any, Union

class BaseService:
    collection_name: str = None
    id_type = ObjectId  # Default to ObjectId, set to int in subclasses if needed

    @classmethod
    def get_collection(cls):
        if not cls.collection_name:
            raise ValueError("Collection name must be defined in the service class")
        return mongo.db[cls.collection_name]

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Union[str, int]:
        result = cls.get_collection().insert_one(data)
        return result.inserted_id

    @classmethod
    def get_all(cls, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        query = query or {}
        cursor = cls.get_collection().find(query)
        return list(cursor)

    @classmethod
    def get_by_id(cls, item_id: Union[str, int]) -> Optional[Dict[str, Any]]:
        try:
            query_id = cls._process_id(item_id)
            return cls.get_collection().find_one({"_id": query_id})
        except Exception:
            return None

    @classmethod
    def update(cls, item_id: Union[str, int], data: Dict[str, Any]) -> bool:
        try:
            query_id = cls._process_id(item_id)
            result = cls.get_collection().update_one(
                {"_id": query_id},
                {"$set": data}
            )
            return result.modified_count > 0
        except Exception:
            return False

    @classmethod
    def delete(cls, item_id: Union[str, int]) -> bool:
        try:
            query_id = cls._process_id(item_id)
            result = cls.get_collection().delete_one({"_id": query_id})
            return result.deleted_count > 0
        except Exception:
            return False

    @classmethod
    def _process_id(cls, item_id: Union[str, int]):
        if cls.id_type == int:
            return int(item_id)
        return ObjectId(item_id)
