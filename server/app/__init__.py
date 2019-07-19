"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import Flask


def create_app() -> Flask:
    """Flask app factory"""
    _app = Flask(__name__)
    return _app


app = create_app()

with app.app_context():
    from app import routes
    from app import api

    routes.add_routes()
    api.create_api()
