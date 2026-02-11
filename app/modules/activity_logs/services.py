from app.core.base_service import BaseService

class ActivityLogService(BaseService):
    collection_name = "activity_logs"
    id_type = int
