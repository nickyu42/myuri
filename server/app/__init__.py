"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
import os


def create_app() -> Flask:
    """Flask app factory"""
    app = Flask(__name__)

    env = os.environ.get('FLASK_ENV', default='production')

    if env == 'testing':
        print('Environment set to "testing". Set to "production" or "development"')

        import sys
        sys.exit(1)

    is_dev = env == 'development'
    app.config.from_object(DevelopmentConfig() if is_dev else ProductionConfig())

    init_app(app)

    if is_dev:
        init_dev(app)

    return app


def init_app(app: Flask):
    from app.database import db
    db.init_app(app)

    from app.views import main_page
    app.register_blueprint(main_page)

    from app.api import api_routes
    app.register_blueprint(api_routes)


def init_dev(app: Flask):
    # allow database access in dev environment for testing
    from app.database.utils import db_cli
    app.cli.add_command(db_cli)

