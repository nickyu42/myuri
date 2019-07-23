"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import Flask


def create_app() -> Flask:
    """Flask app factory"""
    _app = Flask(__name__)

    from app.routes import main_page
    _app.register_blueprint(main_page)

    from app.api import api_bp
    _app.register_blueprint(api_bp)

    return _app


app = create_app()

