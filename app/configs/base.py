import os

class BaseConfig:
    API_TITLE = "Flask API Base"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/flask_base_db")
    
    # JWT Configuration
    JWT_ALGORITHM = "RS256"
    
    # Load keys
    _basedir = os.path.abspath(os.path.dirname(__file__))
    _rootdir = os.path.dirname(os.path.dirname(_basedir))
    
    with open(os.path.join(_rootdir, "keys", "private.pem"), "rb") as f:
        JWT_PRIVATE_KEY = f.read()
        
    with open(os.path.join(_rootdir, "keys", "public.pem"), "rb") as f:
        JWT_PUBLIC_KEY = f.read()
    # Rate Limiter
    RATELIMIT_HEADERS_ENABLED = True
    
    # CORS
    CORS_HEADERS = "Content-Type"
