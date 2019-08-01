"""
Author: Nick Yu
Date created: 19/7/2019
"""
import os
from pathlib import Path
from flask import Flask

from app.config import DevelopmentConfig, ProductionConfig
from app.data import AbstractComicParser, ComicParser


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

    data_folder = os.environ.get('DATA_FOLDER', default='./data')
    comics_path = Path(data_folder)
    init_app(app, ComicParser(comics_path))

    if is_dev:
        init_dev(app)

    return app


def init_app(app: Flask, parser: AbstractComicParser):
    from app.database import db
    db.init_app(app)

    from app.views import main_page
    app.register_blueprint(main_page)

    from app.api import create_api
    app.register_blueprint(create_api(parser))


def init_dev(app: Flask):
    # allow database access in dev environment for testing
    from app.database.utils import db_cli
    app.cli.add_command(db_cli)

