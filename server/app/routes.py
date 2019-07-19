"""
Author: Nick Yu
Date created: 19/7/2019
"""
from app import app


def add_routes():
    @app.route('/')
    def index():
        return 'Hello World'
