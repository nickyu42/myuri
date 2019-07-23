"""
Author: Nick Yu
Date created: 19/7/2019
"""
from flask import request, Blueprint
from flask_restful import Api, Resource


class Catalog(Resource):
    """Endpoint for getting a JSON catalog based on the query given"""

    def get(self):
        args = request.args
        return str(args)


class Info(Resource):
    """Endpoint for getting a JSON object with info on given comic"""

    def get(self, id: int):
        return 'not implemented'


class Page(Resource):
    """Endpoint for getting images from comics"""

    def get(self, id: int, chapter: str, page: int):
        return 'not implemented'


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Catalog, '/c/catalog')
api.add_resource(Info, '/c/info/<int:id>')
api.add_resource(Page, '/c/<int:id>/<string:chapter>/<int:page>')
