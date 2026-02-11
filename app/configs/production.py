from .base import BaseConfig
import os

class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = "production"
    
    # Ensure critical secrets are set in env
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_URI = os.environ.get("MONGO_URI")
    # JWT keys are loaded from files in BaseConfig, ensure files exist in prod
    
    # Security headers, https only, etc.
    SESSION_COOKIE_SECURE = True
