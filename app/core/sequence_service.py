from app.extensions import mongo

class SequenceService:
    @staticmethod
    def get_next_id(collection_name):
        """
        Atomically increments and returns the next integer ID for a given collection.
        """
        sequence = mongo.db.sequences.find_one_and_update(
            {"_id": collection_name},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True
        )
        return sequence["seq"]
