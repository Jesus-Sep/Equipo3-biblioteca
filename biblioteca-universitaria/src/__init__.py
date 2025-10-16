import os
from flask import Flask
from src.extensions import db, migrate

def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    
    _load_config(app, config_name)
    _register_extensions(app)
    _register_blueprints(app)
    _register_cli(app)
    
    return app

def _load_config(app: Flask, config_name: str | None) -> None:
    app.config.from_object("src.config.BaseConfig")
    env_name = config_name or os.environ.get("ENV_CONFIG", "DevelopmentConfig")
    app.config.from_object(f"src.config.{env_name}")

def _register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)

def _register_blueprints(app: Flask) -> None:
    from src.api.biblioteca import biblioteca_bp
    app.register_blueprint(biblioteca_bp, url_prefix="/api")

def _register_cli(app: Flask) -> None:
    from src.cli import register_seed_command
    register_seed_command(app)