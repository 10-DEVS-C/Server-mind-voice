from app.core.base_service import BaseService

class SessionService(BaseService):
    collection_name = "sessions"
    id_type = int
