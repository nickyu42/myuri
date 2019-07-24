"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
import os


def create_app() -> Flask:
    """Flask app factory"""
    _app = Flask(__name__)

    env = os.environ.get('FLASK_ENV', default='production')
    is_dev = env == 'development'
    _app.config.from_object(DevelopmentConfig() if is_dev else ProductionConfig())

    from app.database.db import db
    db.init_app(_app)

    from app.views import main_page
    _app.register_blueprint(main_page)

    from app.api import api_routes
    _app.register_blueprint(api_routes)

    if is_dev:
        # allow database access in dev environment for testing
        from app.database.views import db_routes
        _app.register_blueprint(db_routes)

    return _app


app = create_app()
