from flask import Flask, redirect
from .configs.development import DevelopmentConfig
from .configs.production import ProductionConfig
from .extensions import mongo, api, jwt, cors, limiter
from .middlewares.error_handler import register_error_handlers
from .middlewares.auth import register_jwt_callbacks
from .modules.users.controllers import blp as users_blp
from .modules.auth.controllers import blp as auth_blp
from .modules.roles.controllers import blp as roles_blp
from .modules.profiles.controllers import blp as profiles_blp
from .modules.folders.controllers import blp as folders_blp
from .modules.tags.controllers import blp as tags_blp
from .modules.files.controllers import blp as files_blp
from .modules.audios.controllers import blp as audios_blp
from .modules.transcriptions.controllers import blp as transcriptions_blp
from .modules.ai_analyses.controllers import blp as ai_analyses_blp
from .modules.documents.controllers import blp as documents_blp
from .modules.mindmaps.controllers import blp as mindmaps_blp
from .modules.sessions.controllers import blp as sessions_blp
from .modules.activity_logs.controllers import blp as activity_logs_blp
import os

def create_app(config_class=None):
    app = Flask(__name__)

    if not config_class:
        env = os.environ.get("FLASK_ENV", "development")
        if env == "production":
            app.config.from_object(ProductionConfig)
        else:
            app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(config_class)

    # Initialize Extensions
    mongo.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    
    # Initialize API with Flask-Smorest
    api.init_app(app)

    # Register Blueprints
    api.register_blueprint(auth_blp, url_prefix="/auth")
    api.register_blueprint(users_blp, url_prefix="/users")
    api.register_blueprint(roles_blp, url_prefix="/roles")
    api.register_blueprint(profiles_blp, url_prefix="/profiles")
    api.register_blueprint(folders_blp, url_prefix="/folders")
    api.register_blueprint(tags_blp, url_prefix="/tags")
    api.register_blueprint(files_blp, url_prefix="/files")
    api.register_blueprint(audios_blp, url_prefix="/audios")
    api.register_blueprint(transcriptions_blp, url_prefix="/transcriptions")
    api.register_blueprint(ai_analyses_blp, url_prefix="/ai-analyses")
    api.register_blueprint(documents_blp, url_prefix="/documents")
    api.register_blueprint(mindmaps_blp, url_prefix="/mindmaps")
    api.register_blueprint(sessions_blp, url_prefix="/sessions")
    api.register_blueprint(activity_logs_blp, url_prefix="/activity-logs")

    # Register Middlewares
    register_error_handlers(app)
    register_jwt_callbacks(jwt)

    @app.route("/")
    def index():
        return redirect("/swagger-ui")

    return app
