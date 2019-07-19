"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import current_app as app
from flask import send_file
from flask_restful import Api, Resource


class Dummy(Resource):
    """Dummy endpoint for development"""

    def get(self):
        return send_file('../static/images/xkcd.jpg', mimetype='image/jpg')


def create_api():
    """Initializes api and adds all resources"""
    api = Api(app)

    api.add_resource(Dummy, '/dummy')
