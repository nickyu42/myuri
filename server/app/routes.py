"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import current_app as app


def add_routes():
    @app.route('/')
    def index():
        return 'Hello World'
