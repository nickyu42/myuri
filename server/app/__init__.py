from flask import Flask


def create_app():
    """Flask app factory"""
    _app = Flask(__name__)
    return _app


app = create_app()

from app import routes